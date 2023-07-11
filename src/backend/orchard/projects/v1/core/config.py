from orchard.libs.utils.secret_str import SecretStr, secret_str_hook
import os

import pathlib

import msgspec

# two directories up and then .env
ENV_PATH = pathlib.Path(__file__).resolve().parents[1] / ".env"

from dotenv import dotenv_values

class Config(msgspec.Struct):
    DATABASE_URL: str
    TESTING: bool
    # 32 bytes, base64 encoded
    # from secrets import token_bytes
    # from base64 import b64encode
    # b64encode(token_bytes(32)).decode('utf-8')
    PASETO_KEY_BASE64: SecretStr
    DISCORD_APPLICATION_ID: str
    DISCORD_PUBLIC_KEY: str
    DISCORD_CLIENT_SECRET: SecretStr


DEFAULT_VALUES = {
    "TESTING": False
}

def _get_config():
    init = {
        **DEFAULT_VALUES,
        **dotenv_values(str(ENV_PATH)),
        **os.environ,
    }
    return msgspec.convert(init, Config, strict=False, dec_hook=secret_str_hook)

def config():
    return _get_config()