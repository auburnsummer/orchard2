from typing import BinaryIO
from zipfile import ZipFile

import hashlib

# BUF_SIZE is totally arbitrary, change for your app!

BUF_SIZE = 65536  # lets read stuff in 64kb chunks!


def sha1_facet(file: BinaryIO, **kwargs):
    return _sha1(file)


def _sha1(f: BinaryIO):
    sha1 = hashlib.sha1()
    f.seek(0)
    while True:
        data = f.read(BUF_SIZE)
        if not data:
            break
        sha1.update(data)
    return sha1.hexdigest()
