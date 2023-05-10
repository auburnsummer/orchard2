from sqlmodel import Field, Relationship, SQLModel, create_engine, JSON, Column
from pydantic import BaseModel
from typing import Any


class DiscordGuild(SQLModel, table=True):
    id: str = Field(primary_key=True)
    display_name: str


class DiscordMessage(SQLModel, table=True):
    message_id: str = Field(primary_key=True)
    channel_id: str
    guild_id: str = Field(foreign_key="discordguild.id")


# https://discord.com/developers/docs/reference#error-messages
class DiscordErrorResponse(BaseModel):
    code: int
    message: str
    errors: Any


class OAuthErrorResponse(BaseModel):
    error: str
    error_description: str


class OAuthTokenResponse(BaseModel):
    access_token: str
    expires_in: int
    refresh_token: str
    scope: str
    token_type: str


class DiscordUser(BaseModel):
    id: str
    """id of the discord user."""
    username: str
    """username of the discord user."""
    avatar: str
    """avatar hash of the user. to get the URL: https://cdn.discordapp.com/avatars/{id}/{avatar}.png"""