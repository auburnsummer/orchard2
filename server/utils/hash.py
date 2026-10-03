from __future__ import annotations

import hashlib
from typing import IO

from functools import lru_cache

BUF_SIZE = 65536  # lets read stuff in 64kb chunks!

def checksum(f: IO[bytes], hasher: hashlib._Hash) -> str:
    f.seek(0)
    while True:
        data = f.read(BUF_SIZE)
        if not data:
            break
        hasher.update(data)
    return hasher.hexdigest().lower()

# fyi this will cache iff it's the same object ref, e.g.
# a = BytesIO(b"hello")
# b = BytesIO(b"hello")
# call to sha1(a) and sha1(b) will not cache.

@lru_cache(maxsize=8)
def sha1(f: IO[bytes]) -> str:
    return checksum(f, hashlib.sha1())

@lru_cache(maxsize=8)
def sha256(f: IO[bytes]) -> str:
    return checksum(f, hashlib.sha256())