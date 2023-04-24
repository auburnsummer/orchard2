from sqlmodel import Field, SQLModel, JSON, Column
from typing import List, Optional
import datetime
from vitals.pydantic_model import ColorToken

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
