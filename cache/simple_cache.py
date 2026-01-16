import hashlib
import os


CACHE_DIR = "cache/data"
os.makedirs(CACHE_DIR, exist_ok=True)


def _hash(key):
    return hashlib.md5(key.encode()).hexdigest()


def get_cached(key):
    path = os.path.join(CACHE_DIR, _hash(key))
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return None


def set_cache(key, value):
    path = os.path.join(CACHE_DIR, _hash(key))
    with open(path, "w", encoding="utf-8") as f:
        f.write(value)
