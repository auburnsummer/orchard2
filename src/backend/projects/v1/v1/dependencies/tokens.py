from base64 import b64decode
from typing import Annotated, TypeAlias
from v1.env import ENV
from fastapi import Depends

from pyseto import Key, KeyInterface

def get_paseto_key():
    key_bytes = b64decode(ENV.paseto_key_base64.get_secret_value())
    key = Key.new(version=4, purpose='local', key=key_bytes)
    return key

PasetoKey: TypeAlias = Annotated[KeyInterface, Depends(get_paseto_key)]