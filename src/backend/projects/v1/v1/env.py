from pydantic import BaseSettings, SecretStr, Field

from dotenv import load_dotenv

load_dotenv()

class Environment(BaseSettings):
    discord_client_id: str = Field(..., env="discord_client_id")
    discord_client_secret: SecretStr = Field(..., env="discord_client_secret")

    class Config:
        case_sensitive = False

ENV = Environment()