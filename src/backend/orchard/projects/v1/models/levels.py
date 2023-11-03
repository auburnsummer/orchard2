"""
A Level is a single playable level backed by an rdzip file.

All levels belong to a user and a publisher.
"""

from __future__ import annotations
import asyncio
from datetime import datetime, timedelta
from io import BytesIO
from tempfile import TemporaryFile

from typing import Optional
import httpx
from msgspec import field
import msgspec
from orchard.libs.bunny_storage.bunny_storage import BunnyStorage
from orchard.libs.vitals.pydantic_model import VitalsLevelBase
from orchard.projects.v1.core.auth import AssetURLScope, OrchardAuthScopes, OrchardAuthToken, make_token_now, requires_scopes
from orchard.projects.v1.core.config import config
from orchard.projects.v1.core.forward import forward_httpx
from orchard.projects.v1.models.metadata import metadata
from orchard.libs.vitals import analyze

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
    # might not be the user who posted the level.
    sa.Column("uploader", sa.String, sa.ForeignKey("users.id"), nullable=False),
    sa.Column("publisher", sa.String, sa.ForeignKey("publishers.id"), nullable=False),

    sa.Column("uploaded", sa.DateTime, nullable=False),
    sa.Column("approval", sa.Integer, nullable=False, default=0)
)


class Level(VitalsLevelBase, kw_only=True):
    """
    Corresponding class for Level table.
    """
    image: str
    thumb: str
    icon: Optional[str] = field(default=None)

    url: str
    url2: str

    song_altname: Optional[str] = field(default=None)

    uploader: str
    publisher: str
    uploaded: datetime = field(default_factory=datetime.now)
    approval: int = field(default=0)


class PrefillResult(VitalsLevelBase, kw_only=True):
    image: str
    thumb: str
    url: str
    icon: Optional[str] = None
    asset_token: str

async def run_prefill(source_url: str):
    c = config()
    async with BunnyStorage(
        api_key=c.BUNNY_STORAGE_API_KEY.get_secret_value(),
        base_endpoint=c.BUNNY_STORAGE_HOSTNAME,
        storage_zone_name=c.BUNNY_STORAGE_USERNAME,
        public_cdn_base=c.BUNNY_CDN_URL
    ) as bun:
        with TemporaryFile(mode="w+b") as f:
            async with httpx.AsyncClient() as client:
                resp = await client.get(source_url)
                resp.raise_for_status()
                async for chunk in resp.aiter_bytes():
                    f.write(chunk)
            f.seek(0)
            level = analyze(f)
            # also we have to upload the rdzip now
            # nb the function here also seeks back to 0 already
            # todo: figure out what sorta errors can happen here?
            rdzip_args = f, "levels", "rdzip"
            image_args = BytesIO(level.image), "images", "png"
            icon_args = (BytesIO(level.icon), "icons", "png") if level.icon else None
            thumb_args = BytesIO(level.thumb), "thumbnails", "webp"
            async with asyncio.TaskGroup() as tg:
                tg.create_task(bun.upload_file_by_hash(*rdzip_args))
                tg.create_task(bun.upload_file_by_hash(*image_args))
                tg.create_task(bun.upload_file_by_hash(*thumb_args))
                if icon_args:
                    tg.create_task(bun.upload_file_by_hash(*icon_args))

            thumb = bun.get_public_url(bun.get_url_by_hash(*thumb_args))
            image = bun.get_public_url(bun.get_url_by_hash(*image_args))
            icon = bun.get_public_url(bun.get_url_by_hash(*icon_args) if icon_args else None)
            url = bun.get_public_url(bun.get_url_by_hash(*rdzip_args))
            asset_token = make_token_now(
                scopes=OrchardAuthScopes(
                    Publisher_assets=AssetURLScope(
                        image=image,
                        thumb=thumb,
                        icon=icon,
                        url=url
                    )
                ),
                exp_time=timedelta(days=1)
            )

            payload = {
                **msgspec.structs.asdict(level),
                "thumb": thumb,
                "image": image,
                "icon": icon,
                "url": url,
                "asset_token": asset_token
            }
            to_send = msgspec.convert(payload, PrefillResult)
            return to_send


def add_level():
    pass