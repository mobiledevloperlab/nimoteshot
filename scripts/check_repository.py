#!/usr/bin/env python3
"""Check contribution-critical files, JSON, demo integrity and local Markdown links."""
import hashlib
import json
import re
import subprocess
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = (
    'LICENSE', 'README.md', 'README.zh-CN.md',
    '.github/CODE_OF_CONDUCT.md', '.github/CONTRIBUTING.md', '.github/SECURITY.md',
    'docs/CHANGELOG.md', 'docs/GOVERNANCE.md', 'docs/THIRD_PARTY_NOTICES.md',
    'docs/OPEN_SOURCE_AUDIT.md', 'docs/RELEASING.md',
)


def main():
    errors = []
    for name in REQUIRED:
        if not (ROOT / name).is_file():
            errors.append(f'Missing {name}')
    names = subprocess.check_output(
        ['git', 'ls-files', '-z', '--cached', '--others', '--exclude-standard'], cwd=ROOT,
    ).decode('utf-8').split('\0')
    for name in filter(None, names):
        path = ROOT / name
        if not path.is_file():
            continue
        if (path.name.startswith('.env') and path.name != '.env.example') or path.suffix in ('.pem', '.key', '.p12', '.pfx'):
            errors.append(f'Private material must not be tracked: {name}')
        if name.startswith(('store_screenshots/runs/', '.venv/')) or (name.startswith('screens/') and name != 'screens/README.md'):
            errors.append(f'Local output must not be tracked: {name}')
        if path.suffix == '.json':
            try:
                json.loads(path.read_text(encoding='utf-8'))
            except (ValueError, UnicodeError):
                errors.append(f'Invalid JSON: {name}')
        if path.suffix == '.md':
            text = path.read_text(encoding='utf-8')
            targets = re.findall(r'\[[^\]]*\]\(([^\s)]+)\)', text)
            targets += re.findall(r'(?:href|src)=["\']([^"\']+)["\']', text, flags=re.IGNORECASE)
            for target in targets:
                if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', target) or target.startswith('#'):
                    continue
                local = unquote(target.split('#', 1)[0])
                if not (path.parent / local).exists():
                    errors.append(f'Broken local link: {name} -> {target}')
    manifest = json.loads((ROOT / 'demo/nimotecode/source_manifest.json').read_text(encoding='utf-8'))
    for name, expected in manifest.items():
        path = ROOT / 'demo/nimotecode/originals' / name
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            errors.append(f'Demo manifest mismatch: {name}')
    for error in errors:
        print(error)
    print(f'Repository check: {len(errors)} errors')
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
