from sqlmodel import Field, Relationship, SQLModel, create_engine, JSON, Column
from pydantic import BaseModel


class DiscordGuild(SQLModel, table=True):
    id: str = Field(primary_key=True)
    display_name: str


class DiscordMessage(SQLModel, table=True):
    message_id: str = Field(primary_key=True)
    channel_id: str
    guild_id: str = Field(foreign_key="discordguild.id")


class ErrorResponse(BaseModel):
    error: str
    error_description: str



class DiscordUser(BaseModel):
    id: str
    """id of the discord user."""
    username: str
    """username of the discord user without the #number."""
    avatar: str
    """avatar hash of the user. to get the URL: https://cdn.discordapp.com/avatars/{id}/{avatar}.png"""
    discriminator: str
    """The #number part of the discord user."""
