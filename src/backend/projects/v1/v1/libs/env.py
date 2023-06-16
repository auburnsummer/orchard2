from pydantic import BaseSettings, SecretStr, Field

from dotenv import load_dotenv

load_dotenv()


class Environment(BaseSettings):
    discord_client_id: str = Field(..., env="discord_client_id")
    discord_client_secret: SecretStr = Field(..., env="discord_client_secret")
    discord_bot_api_key: SecretStr = Field(..., env="discord_bot_api_key")
    discord_bot_public_key: str = Field(..., env="discord_bot_public_key")
    discord_bot_application_id: str = Field(..., env="discord_bot_application_id")

    paseto_key_base64: SecretStr = Field(..., env="paseto_key_base64")

    orchard_db_path: str = Field(..., env="orchard_db_path")

    client_url: str = Field(..., env="client_url")

    class Config:
        case_sensitive = False

_environment_singleton: Environment | None = None

def _env():
    global _environment_singleton
    if _environment_singleton is None:
        _environment_singleton = Environment()
    return _environment_singleton

def env():
    return _env()