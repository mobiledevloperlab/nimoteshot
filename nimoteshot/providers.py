"""Vision model adapters for cloud, mainland China, and local providers."""
import base64
import io
import json
import os
import re
import shutil
import subprocess
import tempfile
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlsplit

from PIL import Image

from .settings import profile

MODELS = json.loads((Path(__file__).parent / "models.json").read_text(encoding="utf-8"))
PROVIDERS = {item["id"]: item for item in MODELS["providers"]}


def choice(provider, model="", base_url="", api_key=""):
    if provider not in PROVIDERS:
        raise ValueError("Choose a supported vision provider")
    spec = PROVIDERS[provider]
    saved = profile(provider)
    selected = (model or saved.get("model") or spec["default_model"]).strip()
    if not selected:
        raise ValueError("Enter a vision model ID")
    key = api_key or (os.environ.get(spec["env"], "") if spec["env"] else "") or saved.get("api_key", "")
    protocol = spec["protocol"]
    if protocol not in ("ollama", "codex_cli") and not key:
        raise ValueError(f"Set {spec['env']} or enter this provider's API key")
    if protocol == "openai_compatible":
        endpoint = (base_url or saved.get("base_url") or spec.get("base_url") or "").rstrip("/")
        if not endpoint.startswith("https://"):
            raise ValueError("Enter an HTTPS API base URL")
    elif protocol == "ollama":
        endpoint = (base_url or saved.get("base_url") or spec.get("base_url") or "http://127.0.0.1:11434").rstrip("/")
        parsed = urlsplit(endpoint)
        if (parsed.scheme != "http" or parsed.hostname not in ("127.0.0.1", "localhost")
                or parsed.username or parsed.password or not parsed.port
                or parsed.path or parsed.query or parsed.fragment):
            raise ValueError("Ollama URL must point to localhost")
    else:
        endpoint = ""
    return selected, endpoint, key


def check_connection(provider, model="", base_url="", api_key=""):
    selected, endpoint, key = choice(provider, model, base_url, api_key)
    protocol = PROVIDERS[provider]["protocol"]
    if protocol in ("gemini", "anthropic"):
        if protocol == "gemini":
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{selected}"
            headers = {"x-goog-api-key": key}
        else:
            url = f"https://api.anthropic.com/v1/models/{selected}"
            headers = {"x-api-key": key, "anthropic-version": "2023-06-01"}
        try:
            request = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(request, timeout=12) as response:
                json.load(response)
        except urllib.error.HTTPError as error:
            raise ValueError(f"Provider rejected this key or model (HTTP {error.code})") from error
        except Exception as error:
            raise ValueError(f"Could not reach {provider}: {error}") from error
        return {"ready": True, "message": "Provider and model are reachable", "model": selected}
    if protocol == "openai_compatible":
        return {"ready": True, "message": "Endpoint and credential are configured; model access is checked when generating", "model": selected}
    if protocol == "codex_cli":
        executable = shutil.which("codex")
        if not executable:
            raise ValueError("Codex CLI was not found. Install it and run 'codex login' first.")
        try:
            subprocess.run([executable, "--version"], capture_output=True, text=True, timeout=10, check=True)
        except (OSError, subprocess.SubprocessError) as error:
            raise ValueError("Codex CLI could not start. Run 'codex login' in a terminal, then try again.") from error
        return {"ready": True, "message": "Codex CLI is available; your signed-in account is used when generating", "model": selected}
    try:
        with urllib.request.urlopen(endpoint + "/api/tags", timeout=4) as response:
            tags = json.load(response)
    except Exception as error:
        raise ValueError("Ollama is not running. Install Ollama, then start it with 'ollama serve'.") from error
    installed = [item.get("name") for item in tags.get("models", [])]
    if selected not in installed:
        raise ValueError(f"Model {selected} is missing. Run: ollama pull {selected}")
    return {"ready": True, "message": "Ollama and the selected model are ready", "model": selected}


def _thumbnail(path):
    with Image.open(path) as original:
        original.verify()
    with Image.open(path) as original:
        image = original.convert("RGB")
        image.thumbnail((1280, 1280), Image.Resampling.LANCZOS)
        out = io.BytesIO()
        image.save(out, format="JPEG", quality=78)
    return base64.b64encode(out.getvalue()).decode("ascii")


def _request(url, payload, headers):
    request = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"),
                                     headers={"Content-Type": "application/json", **headers}, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=240) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        raise RuntimeError(f"Vision API rejected the request (HTTP {error.code}). Check quota, credentials and model access.") from None


def _openai_request(endpoint, key, selected, content):
    """Use the maintained OpenAI Python client for OpenAI-compatible APIs."""
    try:
        from openai import OpenAI
    except ImportError as error:
        raise RuntimeError("Install the OpenAI client: pip install openai") from error
    from openai import APIConnectionError, APIStatusError, APITimeoutError
    try:
        with OpenAI(api_key=key, base_url=endpoint, timeout=90, max_retries=2) as client:
            options = {"response_format": {"type": "json_object"}, "max_tokens": 8192} if selected == "deepseek-flash" else {}
            response = client.chat.completions.create(model=selected, messages=[{"role": "user", "content": content}], **options)
            if response.choices[0].finish_reason == 'length':
                raise ValueError('Vision response exceeded the output limit. Use fewer captures or languages.')
            return response.choices[0].message.content
    except APITimeoutError:
        raise RuntimeError('Vision request timed out after retries. Try again or use manual design.') from None
    except APIConnectionError:
        raise RuntimeError('Cannot connect to the vision provider after retries. Check your network or use manual design.') from None
    except APIStatusError as error:
        hints = {401: 'Check your API key.', 403: 'Check model permissions.',
                 429: 'Rate or quota limit reached. Wait and check your balance.'}
        raise RuntimeError(f'Vision API HTTP {error.status_code}. '+hints.get(error.status_code,'Provider request failed after retries; try again later.')) from None


def analyze(files, prompt, provider, model="", base_url="", api_key=""):
    selected, endpoint, key = choice(provider, model, base_url, api_key)
    protocol = PROVIDERS[provider]["protocol"]
    images = [(path.name, _thumbnail(path)) for path in files]
    if protocol == "gemini":
        parts = [{"text": prompt}]
        for name, data in images:
            parts.extend(({"text": f"Filename: {name}"}, {"inline_data": {"mime_type": "image/jpeg", "data": data}}))
        response = _request(f"https://generativelanguage.googleapis.com/v1beta/models/{selected}:generateContent",
                            {"contents": [{"role": "user", "parts": parts}], "generationConfig": {"responseMimeType": "application/json"}},
                            {"x-goog-api-key": key})
        text = "".join(part.get("text", "") for part in response["candidates"][0]["content"]["parts"])
    elif protocol == "anthropic":
        content = [{"type": "text", "text": prompt}]
        for name, data in images:
            content.extend(({"type": "text", "text": f"Filename: {name}"},
                            {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": data}}))
        response = _request("https://api.anthropic.com/v1/messages",
                            {"model": selected, "max_tokens": 4096, "messages": [{"role": "user", "content": content}]},
                            {"x-api-key": key, "anthropic-version": "2023-06-01"})
        text = "".join(part.get("text", "") for part in response["content"] if part.get("type") == "text")
    elif protocol == "ollama":
        response = _request(endpoint + "/api/chat",
                            {"model": selected, "stream": False, "format": "json", "messages": [{"role": "user", "content": prompt + "\nImages in filename order: " + ", ".join(name for name, _ in images), "images": [data for _, data in images]}]}, {})
        text = response["message"]["content"]
    elif protocol == "codex_cli":
        executable = shutil.which("codex")
        if not executable:
            raise ValueError("Codex CLI was not found. Install it and run 'codex login' first.")
        with tempfile.TemporaryDirectory(prefix="nimoteshot-codex-") as temporary:
            output = Path(temporary) / "response.txt"
            command = [executable, "exec", "--skip-git-repo-check", "--sandbox", "read-only", "--ephemeral",
                       "--output-last-message", str(output), "--model", selected, prompt]
            for path in files:
                command.extend(("--image", str(path)))
            try:
                subprocess.run(command, capture_output=True, text=True, timeout=600, check=True)
            except subprocess.TimeoutExpired as error:
                raise RuntimeError("Codex CLI timed out while analyzing captures") from error
            except subprocess.CalledProcessError as error:
                detail = (error.stderr or error.stdout or "Codex CLI failed").strip()[-1200:]
                raise RuntimeError(f"Codex CLI failed: {detail}") from error
            text = output.read_text(encoding="utf-8") if output.is_file() else ""
    else:
        content = [{"type": "text", "text": prompt}]
        for name, data in images:
            content.extend(({"type": "text", "text": f"Filename: {name}"},
                            {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64," + data}}))
        text = _openai_request(endpoint, key, selected, content)
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Vision model returned no text")
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text)
    try:
        return json.loads(text)
    except json.JSONDecodeError as error:
        raise ValueError("Vision model did not return valid JSON; try another model") from error
