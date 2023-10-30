from typing import List, Optional
from datetime import datetime

from .color_tagged_string import ColorToken

import msgspec

class VitalsLevelBase(msgspec.Struct):
    artist: str
    artist_tokens: List[str]
    song: str
    song_ct: List[ColorToken]
    seizure_warning: bool
    description: str
    description_ct: List[ColorToken]
    hue: float
    authors: List[str]
    authors_raw: str
    max_bpm: float
    min_bpm: float
    difficulty: int
    single_player: bool
    two_player: bool
    last_updated: datetime
    tags: List[str]
    has_classics: bool
    has_oneshots: bool
    has_squareshots: bool
    has_freezeshots: bool
    has_freetimes: bool
    has_holds: bool
    has_skipshots: bool
    has_window_dance: bool
    sha1: str
    rdlevel_sha1: str
    is_animated: bool
    
class VitalsLevel(VitalsLevelBase):
    image: bytearray
    thumb: bytearray
    icon: Optional[bytearray]