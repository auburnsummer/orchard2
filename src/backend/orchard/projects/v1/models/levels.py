"""
A Level is a single playable level backed by an rdzip file.

All levels belong to a user and a publisher.
"""

from __future__ import annotations
from datetime import datetime

from typing import Optional
from msgspec import field
from orchard.libs.vitals.pydantic_model import VitalsLevelBase
from orchard.projects.v1.models.metadata import metadata

import sqlalchemy as sa

levels = sa.Table(
    "levels",
    metadata,
    # a generated id
    sa.Column("id", sa.String, primary_key=True),

    # vitals
    sa.Column("artist", sa.String, nullable=False),
    sa.Column("artist_tokens", sa.JSON, nullable=False),
    sa.Column("song", sa.String, nullable=False),
    sa.Column("song_ct", sa.JSON, nullable=False),
    sa.Column("seizure_warning", sa.Boolean, nullable=False),
    sa.Column("description", sa.String, nullable=False),
    sa.Column("description_ct", sa.JSON, nullable=False),
    sa.Column("hue", sa.Float, nullable=False),
    sa.Column("authors", sa.JSON, nullable=False),
    sa.Column("authors_raw", sa.String, nullable=False),
    sa.Column("max_bpm", sa.Float, nullable=False),
    sa.Column("min_bpm", sa.Float, nullable=False),
    sa.Column("difficulty", sa.Integer, nullable=False),
    sa.Column("single_player", sa.Boolean, nullable=False),
    sa.Column("two_player", sa.Boolean, nullable=False),
    sa.Column("last_updated", sa.DateTime, nullable=False),
    sa.Column("tags", sa.JSON, nullable=False),
    sa.Column("has_classics", sa.Boolean, nullable=False),
    sa.Column("has_oneshots", sa.Boolean, nullable=False),
    sa.Column("has_squareshots", sa.Boolean, nullable=False),
    sa.Column("has_freezeshots", sa.Boolean, nullable=False),
    sa.Column("has_freetimes", sa.Boolean, nullable=False),
    sa.Column("has_holds", sa.Boolean, nullable=False),
    sa.Column("has_skipshots", sa.Boolean, nullable=False),
    sa.Column("has_window_dance", sa.Boolean, nullable=False),
    sa.Column("sha1", sa.String, nullable=False, unique=True),
    sa.Column("rdlevel_sha1", sa.String, nullable=False, unique=True),

    # not quite from vitals but derived data
    sa.Column("image", sa.String, nullable=False),
    sa.Column("thumb", sa.String, nullable=False),
    sa.Column("icon", sa.String, nullable=True),
    sa.Column("url", sa.String, nullable=False),
    sa.Column("url2", sa.String, nullable=False),

    # e.g localised title if song is CJK
    sa.Column("song_altname", sa.String, nullable=True),

    # other stuff.
    sa.Column("user", sa.String, sa.ForeignKey("users.id"), nullable=False),
    sa.Column("publisher", sa.String, sa.ForeignKey("publishers.id"), nullable=False),

    sa.Column("uploaded", sa.DateTime, nullable=False),
    sa.Column("approval", sa.Integer, nullable=False, default=0)
)

class Level(VitalsLevelBase):
    image: str
    thumb: str
    icon: Optional[str] = field(default=None)

    url: str
    url2: str

    song_altname: Optional[str] = field(default=None)

    user: str
    publisher: str
    uploaded: datetime = field(default_factory=datetime.now)
    approval: int = field(default=0)

