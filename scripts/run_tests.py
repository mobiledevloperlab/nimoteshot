#!/usr/bin/env python3
"""Run the unittest suite and surface tracebacks in GitHub check annotations."""
import io
import os
import sys
import unittest
from pathlib import Path

# Preserve multilingual diagnostics on Windows consoles and captured CI streams.
for stream in (sys.stdout, sys.stderr):
    if hasattr(stream, 'reconfigure'):
        stream.reconfigure(encoding='utf-8', errors='backslashreplace')

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def main():
    stream = io.StringIO()
    suite = unittest.defaultTestLoader.discover("tests")
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    output = stream.getvalue()
    print(output, end="")
    if result.wasSuccessful():
        return 0
    if os.environ.get("GITHUB_ACTIONS") == "true":
        escaped = output[-12000:].replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
        print(f"::error title=Unit tests failed::{escaped}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
