"""Content-addressed vision analysis cache; no credentials are stored."""
import hashlib
import json

from diskcache import Cache, Lock

TTL = 7 * 24 * 60 * 60
MAX_BYTES = 64 * 1024 * 1024


def cached_analysis(directory, identity, produce, validate, progress=lambda _: None, refresh=False):
    key = hashlib.sha256(json.dumps(identity, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    with Cache(str(directory), size_limit=MAX_BYTES, eviction_policy='least-recently-used') as cache:
        with Lock(cache, 'lock:' + key, expire=600):
            cache.expire()
            value = None if refresh else cache.get(key)
            if value is not None:
                try:
                    result = validate(json.loads(value))
                    progress('Reusing cached screenshot analysis')
                    return result
                except (ValueError, TypeError):
                    cache.delete(key)
            result = validate(produce())
            cache.set(key, json.dumps(result, ensure_ascii=False), expire=TTL)
            return result
