"""Local provider profiles kept outside the repository and generated output."""
import json
import os
import stat
import tempfile
from pathlib import Path


def config_path():
    if os.name == "nt":
        base = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
        return base / "NimoteShot" / "config.json"
    base = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
    return base / "nimoteshot" / "config.json"


def load():
    path = config_path()
    if not path.is_file():
        return {"profiles": {}}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"profiles": {}}
    return value if isinstance(value, dict) and isinstance(value.get("profiles"), dict) else {"profiles": {}}


def profile(provider):
    value = load()["profiles"].get(provider, {})
    return value if isinstance(value, dict) else {}


def has_key(provider):
    return bool(profile(provider).get("api_key"))


def save(provider, model="", base_url="", api_key="", clear_key=False):
    value = load()
    current = value["profiles"].get(provider, {})
    updated = {**current}
    if model:
        updated["model"] = model
    if base_url:
        updated["base_url"] = base_url
    if api_key:
        updated["api_key"] = api_key
    if clear_key:
        updated.pop("api_key", None)
    value["profiles"][provider] = updated
    path = config_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    # mkstemp creates a private file before any credential bytes are written.
    # Replace atomically so readers never see partial JSON or follow a symlink.
    fd, temporary = tempfile.mkstemp(prefix=".config-", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            if os.name != "nt":
                os.fchmod(stream.fileno(), stat.S_IRUSR | stat.S_IWUSR)
            stream.write(json.dumps(value, ensure_ascii=False, indent=2) + "\n")
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
    return path


def describe():
    return {name: {"model": item.get("model", ""), "base_url": item.get("base_url", ""),
                   "has_api_key": bool(item.get("api_key"))} for name, item in load()["profiles"].items()}
