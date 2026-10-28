"""Content-addressed JSON vision cache; no credentials or executable objects are stored."""
import hashlib
import json
import os
import tempfile
import time
from contextlib import contextmanager
from pathlib import Path

TTL = 7 * 24 * 60 * 60
MAX_BYTES = 64 * 1024 * 1024
LOCK_STALE_AFTER = 600
LOCK_WAIT = 30


def _remove(path):
    try:
        path.unlink()
    except FileNotFoundError:
        pass


@contextmanager
def _key_lock(directory, key):
    """Use atomic creation for a portable per-key process lock."""
    path = directory / f"{key}.lock"
    deadline = time.monotonic() + LOCK_WAIT
    while True:
        try:
            descriptor = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
            with os.fdopen(descriptor, "w", encoding="ascii") as stream:
                stream.write(str(os.getpid()))
            break
        except FileExistsError:
            try:
                if time.time() - path.stat().st_mtime > LOCK_STALE_AFTER:
                    _remove(path)
                    continue
            except FileNotFoundError:
                continue
            if time.monotonic() >= deadline:
                raise TimeoutError("Timed out waiting for the analysis cache")
            time.sleep(0.05)
    try:
        yield
    finally:
        _remove(path)


def _read(path, validate):
    if path.is_symlink():
        raise ValueError("Cache entries must be regular files")
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or not isinstance(payload.get("expires_at"), (int, float)):
        raise ValueError("Invalid cache entry")
    if payload["expires_at"] <= time.time():
        raise ValueError("Expired cache entry")
    result = validate(payload.get("value"))
    os.utime(path, None)
    return result


def _write(path, result):
    payload = json.dumps({"expires_at": time.time() + TTL, "value": result}, ensure_ascii=False)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.stem}-", suffix=".tmp", dir=path.parent)
    temporary = Path(temporary)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        _remove(temporary)


def _prune(directory):
    entries = []
    now = time.time()
    for path in directory.glob("*.json"):
        try:
            if path.is_symlink():
                raise ValueError
            payload = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(payload, dict) or payload.get("expires_at", 0) <= now:
                raise ValueError
            stat = path.stat()
            entries.append((stat.st_mtime, stat.st_size, path))
        except (OSError, ValueError, TypeError, json.JSONDecodeError):
            _remove(path)
    total = sum(size for _, size, _ in entries)
    for _, size, path in sorted(entries):
        if total <= MAX_BYTES:
            break
        _remove(path)
        total -= size


def cached_analysis(directory, identity, produce, validate, progress=lambda _: None, refresh=False):
    key = hashlib.sha256(json.dumps(identity, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{key}.json"
    with _key_lock(directory, key):
        _prune(directory)
        if not refresh and path.is_file():
            try:
                result = _read(path, validate)
                progress("Reusing cached screenshot analysis")
                return result
            except (OSError, ValueError, TypeError, json.JSONDecodeError):
                _remove(path)
        result = validate(produce())
        _write(path, result)
        _prune(directory)
        return result
