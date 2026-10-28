#!/usr/bin/env python3
"""Scan tracked text and optionally reachable Git blobs; never print secret values."""
import argparse
import subprocess
from pathlib import Path

from detect_secrets.core.scan import scan_line
from detect_secrets.settings import default_settings

ROOT = Path(__file__).resolve().parents[1]


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def scan(data, label):
    if b'\0' in data:
        return 0
    try:
        text = data.decode('utf-8')
    except UnicodeDecodeError:
        return 0
    count = 0
    for number, line in enumerate(text.splitlines(), 1):
        for secret in scan_line(line):
            # Only locations and detector types are emitted, never source lines.
            print(f'{label}:{number}: {secret.type}')
            count += 1
    return count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--history', action='store_true')
    args = parser.parse_args()
    count = 0
    with default_settings() as settings:
        # Content hashes/manifests and generic variable names are not credentials.
        # Provider patterns, private keys and basic-auth detectors remain enabled.
        for name in ('Base64HighEntropyString', 'HexHighEntropyString', 'KeywordDetector'):
            settings.disable_plugins(name)
        for raw in git('ls-files', '-z', '--cached', '--others', '--exclude-standard').split(b'\0'):
            if raw:
                path = ROOT / raw.decode('utf-8')
                if path.is_file():
                    count += scan(path.read_bytes(), str(path.relative_to(ROOT)))
        if args.history:
            objects = git('rev-list', '--objects', '--all').splitlines()
            for row in objects:
                oid = row.split(b' ', 1)[0].decode('ascii')
                if git('cat-file', '-t', oid).strip() == b'blob':
                    count += scan(git('cat-file', 'blob', oid), 'git-blob:' + oid)
    print(f'Secret scan: {count} findings. Binary assets and generic secrets require manual review.')
    return bool(count)


if __name__ == '__main__':
    raise SystemExit(main())
