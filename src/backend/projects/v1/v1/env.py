from pydantic import BaseSettings, SecretStr, Field

from dotenv import load_dotenv

from base64 import b64decode

load_dotenv()

class Environment(BaseSettings):
    discord_client_id: str = Field(..., env="discord_client_id")
    discord_client_secret: SecretStr = Field(..., env="discord_client_secret")
    discord_bot_api_key: SecretStr = Field(..., env="discord_bot_api_key")

    paseto_key_base64: SecretStr = Field(..., env="paseto_key_base64")

    class Config:
        case_sensitive = False

ENV = Environment()
 