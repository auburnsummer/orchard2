from typing import List, Optional, Annotated
from datetime import datetime

import msgspec

class VitalsLevelBaseMutable(msgspec.Struct):
    "The properties on VitalsLevel where it might make sense for the client to be changing them"
    artist: str
    artist_tokens: Annotated[List[str], msgspec.Meta(min_length=1)]
    song: Annotated[str, msgspec.Meta(min_length=1)]
    seizure_warning: bool
    description: str
    hue: float
    authors: Annotated[List[str], msgspec.Meta(min_length=1)]
    max_bpm: int
    min_bpm: int
    difficulty: int
    single_player: bool
    two_player: bool
    tags: List[str]
    has_classics: bool
    has_oneshots: bool
    has_squareshots: bool
    has_freezeshots: bool
    has_freetimes: bool
    has_holds: bool
    has_skipshots: bool
    has_window_dance: bool

class VitalsLevelBase(VitalsLevelBaseMutable):
    "VitalsLevelBaseMutable + immutable properties / properties that are managed by us"
    sha1: str
    rdlevel_sha1: str
    is_animated: bool
    last_updated: datetime
    artist_raw: str
    song_raw: str
    authors_raw: str
    rd_md5: str
    
class VitalsLevel(VitalsLevelBase):
    "VitalsLevelBaseMutable + VitalsLevelBase + image data"
    image: bytearray
    thumb: bytearray
    icon: Optional[bytearray]