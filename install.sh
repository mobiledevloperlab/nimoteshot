#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")"
if command -v python3 >/dev/null 2>&1; then PYTHON=python3; else PYTHON=python; fi
"$PYTHON" -c 'import sys; assert sys.version_info >= (3,11), "Python 3.11 or newer is required"'
if [ ! -f .venv/bin/python ]; then "$PYTHON" -m venv .venv; fi
.venv/bin/python -c 'import sys; assert sys.version_info >= (3,11), "Recreate .venv with Python 3.11 or newer"'
.venv/bin/python -m pip install -r store_screenshots/requirements.txt
exec .venv/bin/python scripts/nimoteshot.py web "$@"
