import datetime
from sqlmodel import Field, Relationship, SQLModel, create_engine, JSON, Column
from v1.models.discord import DiscordUser


class User(SQLModel, table=True):
    discord_id: str = Field(primary_key=True)
    "id of the user"
    logout_time: datetime.datetime = Field(default=datetime.datetime.fromtimestamp(0))
    "tokens issued before this time are invalid."


class UserCombined(User, DiscordUser):
    pass