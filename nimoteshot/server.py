"""Local-only web API for planning, preview and deterministic export."""
import io
import hmac
import base64
import json
import mimetypes
import os
import shutil
import tempfile
import threading
from datetime import datetime, timezone
import uuid
import webbrowser
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import unquote, urlsplit

from .pipeline import LOCALES, OUTPUT_LOCALES, MODELS, ROOT, RUNS, STYLES, TARGET_NAMES, generate, prepare_context, plan, build_config, renderer
from .captures import unpack
from .design import TEMPLATES
from .planner import revise
from .providers import check_connection
from .settings import describe, has_key, save
from .web_runtime import bind_studio, runtime_token_path, signature

WEB = ROOT / "web"
PUBLIC_DOCUMENTS = {
    "guide": "README.md",
    "guide-zh": "README.zh-CN.md",
    "license": "LICENSE",
    "contributing": ".github/CONTRIBUTING.md",
    "security": ".github/SECURITY.md",
    "notices": "docs/THIRD_PARTY_NOTICES.md",
}
PUBLIC_DOCUMENT_TITLES = {
    "guide": "User guide",
    "guide-zh": "使用指南",
    "contributing": "参与贡献",
    "security": "安全与数据",
    "license": "许可证",
    "notices": "第三方声明",
}
JOBS = {}
LOCK = threading.Lock()
MAX_REQUEST = 250 * 1024 * 1024


def job_event(job_id, message, status="running"):
    """Append safe, user-facing lifecycle events; never include prompts or credentials."""
    event = {"message": message, "at": datetime.now(timezone.utc).isoformat(timespec="seconds")}
    with LOCK:
        job = JOBS[job_id]
        job["status"] = status
        job["message"] = message
        if message.startswith("Rendering "):
            job["rendered"] = job.get("rendered", 0) + 1
            total = max(1, job.get("total_renders", 1))
            job["progress"] = min(90, 20 + round(70 * job["rendered"] / total))
        else:
            job["progress"] = max(job.get("progress", 0), {
                "Preparing captures": 3, "Validating PNG/JPEG/WebP captures": 10,
                "Analyzing captures with AI": 20, "Reusing cached screenshot analysis": 45,
                "Archiving verified originals": 15, "Packaging and validating ZIP": 95,
                "Complete": 100,
            }.get(message, 12 if message.startswith("Revising ") else 0))
        job.setdefault("events", []).append(event)


def safe_error(error, payload):
    """A provider may echo request data; never return a submitted credential."""
    message=str(error)
    key=payload.get('api_key') if isinstance(payload,dict) else None
    return message.replace(key,'[REDACTED]') if isinstance(key,str) and key else message


class Handler(BaseHTTPRequestHandler):
    def local_request(self):
        # An attacker-controlled hostname can resolve to loopback (DNS rebinding).
        # Check Host on reads as well as writes, before exposing local data.
        port = self.server.server_address[1]
        allowed = {f"127.0.0.1:{port}", f"localhost:{port}"}
        host = self.headers.get("Host", "")
        if len(self.headers.get_all("Host", [])) != 1 or host not in allowed:
            self.json_response({"error": "Only local studio hosts are allowed"}, 403)
            return False
        origin = self.headers.get("Origin")
        if origin and origin != f"http://{host}":
            self.json_response({"error": "Cross-origin requests are disabled"}, 403)
            return False
        if self.headers.get("Sec-Fetch-Site") == "cross-site":
            self.json_response({"error": "Cross-site requests are disabled"}, 403)
            return False
        return True

    def log_message(self, fmt, *args):
        # Do not log request bodies or API credentials.
        print("[web] " + fmt % args)

    def json_response(self, value, status=200):
        data = json.dumps(value, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def file_response(self, path, content_type=None):
        if not path.is_file():
            self.send_error(404)
            return
        content_type = content_type or mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(path.stat().st_size))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        with path.open("rb") as stream:
            shutil.copyfileobj(stream, self.wfile)

    def do_GET(self):
        if not self.local_request():
            return
        path = unquote(urlsplit(self.path).path)
        if path == "/api/studio":
            token = getattr(self.server, 'studio_token', None)
            challenge = self.headers.get('X-NimoteShot-Challenge', '')
            if not token or len(challenge) != 64 or any(c not in '0123456789abcdef' for c in challenge):
                self.json_response({'error': 'Studio identity unavailable'}, 404)
                return
            instance = self.server.studio_instance
            self.json_response({'instance': instance, 'proof': signature(token, 'identity:' + challenge + ':' + instance)})
        elif path == "/api/options":
            sources = {}
            for item in MODELS["providers"]:
                if not item["env"]:
                    sources[item["id"]] = "cli" if item["protocol"] == "codex_cli" else "none"
                elif os.environ.get(item["env"]):
                    sources[item["id"]] = "environment"
                elif has_key(item["id"]):
                    sources[item["id"]] = "profile"
                else:
                    sources[item["id"]] = "none"
            self.json_response({"models": MODELS, "styles": STYLES, "credential_source": sources,
                                "profiles": describe(), "templates": TEMPLATES, "output_locales": OUTPUT_LOCALES, "text_shaping": renderer.features.check('raqm')})
        elif path.startswith("/api/docs/"):
            slug = path.removeprefix("/api/docs/")
            name = PUBLIC_DOCUMENTS.get(slug)
            if name is None:
                self.send_error(404)
            else:
                source = ROOT / name
                self.json_response({"slug": slug, "title": PUBLIC_DOCUMENT_TITLES[slug],
                                    "source": name, "content": source.read_text(encoding="utf-8")})
        elif path.startswith("/docs/"):
            slug = path.removeprefix("/docs/")
            if slug not in PUBLIC_DOCUMENTS:
                self.send_error(404)
            else:
                self.file_response(WEB / "docs.html", "text/html; charset=utf-8")
        elif path.startswith("/api/jobs/"):
            job_id = path.removeprefix("/api/jobs/")
            with LOCK:
                job = JOBS.get(job_id)
                result = dict(job) if job else None
            self.json_response(result if result else {"error": "Job not found"}, 200 if result else 404)
        elif path.startswith("/files/"):
            candidate = (RUNS / path.removeprefix("/files/")).resolve()
            if not candidate.is_relative_to(RUNS.resolve()):
                self.send_error(403)
            else:
                self.file_response(candidate)
        elif path == "/assets/Inter.ttf":
            self.file_response(ROOT / "store_screenshots/assets/fonts/Inter.ttf")
        elif path.startswith("/assets/demo-previews/"):
            filename = path.removeprefix("/assets/demo-previews/")
            previews = (ROOT / "demo/nimotecode/previews").resolve()
            candidate = (previews / filename).resolve()
            if candidate.is_relative_to(previews) and candidate.suffix.lower() == ".png":
                self.file_response(candidate)
            else:
                self.send_error(403)
        else:
            relative = "index.html" if path == "/" else path.lstrip("/")
            candidate = (WEB / relative).resolve()
            if not candidate.is_relative_to(WEB.resolve()):
                self.send_error(403)
            else:
                self.file_response(candidate)

    def do_POST(self):
        if not self.local_request():
            return
        route = urlsplit(self.path).path
        small_routes = ('/api/preflight', '/api/configure', '/api/check-model', '/api/open-output', '/api/studio/shutdown')
        if route not in (*small_routes, '/api/generate', '/api/plan', '/api/revise', '/api/preview'):
            self.send_error(404)
            return
        if self.headers.get('Transfer-Encoding') or len(self.headers.get_all('Content-Length', [])) != 1:
            self.json_response({'error': 'A single Content-Length is required'}, 400)
            return
        try:
            length = int(self.headers.get('Content-Length', '0'))
            if not 0 < length <= (10000 if route in small_routes else MAX_REQUEST):
                self.json_response({'error': 'Request exceeds the allowed size'}, 413)
                return
            payload = json.loads(self.rfile.read(length))
            if not isinstance(payload, dict):
                raise ValueError('Request body must be a JSON object')
            if route == '/api/studio/shutdown':
                token = getattr(self.server, 'studio_token', None)
                instance = getattr(self.server, 'studio_instance', None)
                proof = payload.get('proof')
                if (not token or payload.get('instance') != instance or not isinstance(proof, str)
                        or len(proof) != 64 or any(c not in '0123456789abcdef' for c in proof)
                        or not hmac.compare_digest(proof, signature(token, 'shutdown:' + instance))):
                    self.json_response({'error': 'Studio verification failed'}, 403)
                    return
                with LOCK:
                    if any(job['status'] in ('queued', 'running') for job in JOBS.values()):
                        self.json_response({'error': 'Studio has active tasks'}, 409)
                        return
                    self.server.studio_draining = True
                self.json_response({'stopping': True})
                threading.Thread(target=self.server.shutdown, daemon=True).start()
                return
            if route == '/api/open-output':
                run_id = payload.get('run_id', '')
                if not isinstance(run_id, str) or len(run_id) != 22 or not all(character.isalnum() or character == '-' for character in run_id):
                    raise ValueError('Invalid output folder')
                output = (RUNS / run_id / 'exports').resolve()
                if not output.is_relative_to(RUNS.resolve()) or not output.is_dir():
                    raise ValueError('Output folder not found')
                if not webbrowser.open(output.as_uri()):
                    raise OSError('Could not open the output folder')
                self.json_response({'opened': True, 'path': str(output)})
                return
            # Reject non-string options before provider code or filesystem operations.
            for key in ('brand','description','website_url','design_prompt','provider','model','base_url','api_key','style','action','source_profile','analysis_language'):
                if key in payload and not isinstance(payload[key], str):
                    raise ValueError(f'{key} must be text')
            provider = payload.get('provider', MODELS['default_provider'])
            model_args = (provider, payload.get('model',''), payload.get('base_url',''), payload.get('api_key',''))
            if route in ('/api/check-model','/api/configure'):
                status = check_connection(*model_args)
                if route == '/api/configure':
                    path = save(*model_args)
                    status.update(saved=True, config_path=str(path), message='Configuration saved locally. '+status['message'])
                self.json_response(status)
                return
            brand, description, website_url, website_text = prepare_context(payload.get('brand'), payload.get('description'), payload.get('website_url'))
            locales = payload.get('locales', ['zh-CN'])
            targets = payload.get('targets', list(TARGET_NAMES))
            if not isinstance(locales,list) or not all(isinstance(v,str) for v in locales) or not set(locales).issubset(LOCALES):
                raise ValueError('Choose supported output languages')
            if not isinstance(targets,list) or not targets or not all(isinstance(v,str) for v in targets) or not set(targets).issubset(TARGET_NAMES):
                raise ValueError('Choose supported output targets')
            style = payload.get('style', STYLES['default'])
            if style not in {v['id'] for v in STYLES['styles']}:
                raise ValueError('Choose a supported design style')
            source_profile = payload.get('source_profile','iphone_portrait')
            if source_profile not in TARGET_NAMES:
                raise ValueError('Choose a supported source capture profile')
            if len(payload.get('design_prompt','')) > 2000:
                raise ValueError('Design direction must be at most 2000 characters')
            if route == '/api/preflight':
                status = ({'ready':True,'message':'Manual design','model':'local'} if payload.get('proposal') or payload.get('manual') else check_connection(*model_args))
                self.json_response({**status,'website_excerpt':website_text[:300]})
                return
            if route == '/api/preview':
                with tempfile.TemporaryDirectory(prefix='nimoteshot-preview-') as temporary:
                    files = unpack(payload.get('files'), temporary)
                    config = build_config('20000101-000000-abcdef',brand,files,payload.get('proposal'),style,tuple(locales),tuple(targets))
                    config['source_dir'] = temporary
                    language = payload.get('preview_locale','en-US')
                    target = payload.get('preview_target',targets[0])
                    if language not in ('en-US',*locales) or target not in targets:
                        raise ValueError('Choose a selected preview language and device')
                    indices = payload.get('preview_indices', list(range(len(config['screens']))))
                    if (not isinstance(indices, list) or not indices
                            or any(type(index) is not int or not 0 <= index < len(config['screens']) for index in indices)
                            or len(set(indices)) != len(indices)):
                        raise ValueError('Choose valid, distinct preview screen indices')
                    config = renderer.localized(config,language)
                    preset = renderer.targets(config)[target]
                    width,height = preset['sizes'][0]
                    size = (round(width*min(480/width,720/height)),round(height*min(480/width,720/height)))
                    render = renderer.render if preset['layout']=='portrait' else renderer.render_landscape
                    pictures=[]
                    # Keep the full config: numbering and duo sources depend on it.
                    for index in indices:
                        image=render(config,config['screens'][index],size,target)
                        buffer=io.BytesIO(); image.save(buffer,format='PNG')
                        pictures.append('data:image/png;base64,'+base64.b64encode(buffer.getvalue()).decode())
                    self.json_response({'images':pictures,'indices':indices,'locale':language,'target':target})
                return
        except (KeyError, ValueError, TypeError, OSError, AssertionError) as error:
            self.json_response({'error': safe_error(error,payload if 'payload' in locals() else {})},400)
            return

        job_id=uuid.uuid4().hex
        with LOCK:
            if getattr(self.server, 'studio_draining', False):
                self.json_response({'error': 'Studio is restarting; retry on the new server'}, 409)
                return
            JOBS[job_id]={'status':'queued','message':'Preparing captures','events':[], 'progress':0,
                          'total_renders':max(1,(len(locales)+1)*len(targets))}

        def worker():
            try:
                if route == '/api/revise':
                    job_event(job_id,'Revising '+payload.get('action','copy')+' from recorded visual evidence')
                    # Validate upload and current design before making a paid copy request.
                    with tempfile.TemporaryDirectory(prefix='nimoteshot-revise-') as temporary:
                        files=unpack(payload.get('files'),temporary)
                        build_config('20000101-000000-abcdef',brand,files,payload.get('proposal'),style,tuple(locales),tuple(targets))
                        proposal=revise(payload.get('proposal'),payload.get('action'),brand,description,
                                        [LOCALES[v]['code'] for v in locales],*model_args)
                        build_config('20000101-000000-abcdef',brand,files,proposal,style,tuple(locales),tuple(targets))
                    result={'proposal':proposal}
                else:
                    with tempfile.TemporaryDirectory(prefix='nimoteshot-') as temporary:
                        job_event(job_id,'Validating PNG/JPEG/WebP captures')
                        unpack(payload.get('files'),temporary)
                        options=dict(style=style,provider=provider,api_key=payload.get('api_key',''),model=payload.get('model',''),
                                     base_url=payload.get('base_url',''),progress=lambda message:job_event(job_id,message),
                                     design_prompt=payload.get('design_prompt',''),locales=tuple(locales),
                                     targets=tuple(targets),source_profile=source_profile,analysis_language=payload.get('analysis_language','en'))
                        if route == '/api/plan':
                            proposal=plan(temporary,brand,description,website_url,**options,refresh=bool(payload.get('refresh')))
                            result={'proposal':proposal}
                        else:
                            result=generate(temporary,brand,description,website_url,**options,proposal=payload.get('proposal'))
                with LOCK:
                    JOBS[job_id].update(status='complete',message='Complete',progress=100,result=result)
            except Exception as error:
                message=safe_error(error,payload)
                with LOCK:
                    JOBS[job_id].update(status='error',message=message)
                    JOBS[job_id].setdefault('events',[]).append({'message':message,'at':datetime.now(timezone.utc).isoformat()})

        threading.Thread(target=worker,daemon=True).start()
        self.json_response({'job_id':job_id},202)


def serve(host="127.0.0.1", port=8765, open_browser=True):
    if host not in ("127.0.0.1", "localhost"):
        raise ValueError("The studio must listen on 127.0.0.1 or localhost")
    server = bind_studio(host, port, Handler, runtime_token_path(ROOT))
    address = f"http://{host}:{server.server_address[1]}"
    print(f"NimoteShot ready at {address}")
    if open_browser:
        threading.Timer(0.6, lambda: webbrowser.open(address)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
