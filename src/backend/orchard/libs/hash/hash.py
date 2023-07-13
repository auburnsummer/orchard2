from __future__ import annotations

import hashlib
from typing import IO, TYPE_CHECKING

from functools import lru_cache

BUF_SIZE = 65536  # lets read stuff in 64kb chunks!

if TYPE_CHECKING:
    from _typeshed import ReadableBuffer

    class _Hash(object):
        """Copied from Typeshed. Typeshed doesn't export this."""
        digest_size: int
        block_size: int

        name: str
        def __init__(self, data: ReadableBuffer = ...) -> None: ...
        def copy(self) -> _Hash: ...
        def digest(self) -> bytes: ...
        def hexdigest(self) -> str: ...
        def update(self, __data: ReadableBuffer) -> None: ...


def checksum(f: IO[bytes], hasher: _Hash) -> str:
    f.seek(0)
    while True:
        data = f.read(BUF_SIZE)
        if not data:
            break
        hasher.update(data)
    return hasher.hexdigest().lower()

# fyi this will cache if it's the same object ref, e.g.
# a = BytesIO(b"hello")
# b = BytesIO(b"hello")
# call to sha1(a) and sha1(b) will not cache.

@lru_cache(maxsize=8)
def sha1(f: IO[bytes]) -> str:
    return checksum(f, hashlib.sha1())

@lru_cache(maxsize=8)
def sha256(f: IO[bytes]) -> str:
    return checksum(f, hashlib.sha256())