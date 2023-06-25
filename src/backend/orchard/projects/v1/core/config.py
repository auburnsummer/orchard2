from pydantic import BaseModel, SecretStr

import os

from dotenv import dotenv_values

class Config(BaseModel):
    DATABASE_URL: str
    TESTING: bool
    # 32 bytes, base64 encoded
    # from secrets import token_bytes
    # from base64 import b64encode
    # b64encode(token_bytes(32)).decode('utf-8')
    PASETO_KEY_BASE64: SecretStr


DEFAULT_VALUES = {
    "TESTING": False
}

def _get_config():
    return Config(
        **DEFAULT_VALUES,
        **dotenv_values(),
        **os.environ
    )

def config():
    return _get_config()