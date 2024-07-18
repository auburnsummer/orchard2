from typing import BinaryIO

from utils.hash import sha1

# BUF_SIZE is totally arbitrary, change for your app!

BUF_SIZE = 65536  # lets read stuff in 64kb chunks!


def sha1_facet(file: BinaryIO, **kwargs):
    return sha1(file).lower()