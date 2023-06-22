from pydantic import BaseModel

import os

from dotenv import dotenv_values

class Config(BaseModel):
    DATABASE_URL: str
    TESTING: bool


DEFAULT_VALUES = {
    "TESTING": False
}

def _get_config():
    return Config(
        **DEFAULT_VALUES,
        **dotenv_values(".env"),
        **os.environ
    )

def config():
    return _get_config()