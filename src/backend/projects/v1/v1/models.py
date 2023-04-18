# SQL models.

import datetime
from typing import Optional, List

from sqlmodel import Field, Relationship, SQLModel, create_engine, JSON, Column

from vitals.pydantic_model import ColorToken


class User(SQLModel, table=True):
    discord_id: str = Field(primary_key=True)
    # should levels this user posts to #rd-showcase be automatically added?
    autoadd_preference: bool


class DiscordMessage(SQLModel, table=True):
    message_id: str = Field(primary_key=True)
    channel_id: str
    guild_id: str


# distinct from VitalsLevel model
class Level(SQLModel, table=True):
    rdlevel_sha1: str = Field(primary_key=True)

    artist: str
    artist_tokens: List[str] = Field(sa_column=Column(JSON))
    authors: List[str] = Field(sa_column=Column(JSON))
    authors_raw: str
    description: str
    description_ct: List[ColorToken] = Field(sa_column=Column(JSON))
    difficulty: int

    discord_message_id: Optional[str] = Field(default=None, foreign_key="discordmessage.message_id")
    discord_attachment_id: Optional[str] = Field(default=None)

    has_classics: bool
    has_freetimes: bool
    has_freezeshots: bool
    has_holds: bool
    has_oneshots: bool
    has_squareshots: bool
    has_skipshots: bool
    has_window_dance: bool

    hue: float
    icon: Optional[str] = Field(default=None)
    image: str
    last_updated: datetime.datetime
    max_bpm: float
    min_bpm: float

    single_player: bool
    sha1: str
    song: str
    song_ct: List[ColorToken] = Field(sa_column=Column(JSON))

    seizure_warning: bool
    tags: List[str] = Field(sa_column=Column(JSON))

    thumb: str
    two_player: bool

    user_id: Optional[str] = Field(default=None, foreign_key="user.discord_id")

    # Needed for Column(JSON)
    class Config:
        arbitrary_types_allowed = True


class Status(SQLModel, table=True):
    alias: str = Field(primary_key=True)

    level_id: str = Field(foreign_key="level.rdlevel_sha1")

    approval: int = Field(default=0)
    approval_thread: Optional[str] = Field(default=None)

    approved_time: Optional[datetime.datetime] = Field(default=None)




sqlite_file_name = "orchard.sqlite3"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)