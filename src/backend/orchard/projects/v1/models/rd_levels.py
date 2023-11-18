"""
A Level is a single playable level backed by an rdzip file.

All levels belong to a user and a publisher.
"""

from __future__ import annotations
import asyncio
from datetime import datetime, timedelta, timezone
from io import BytesIO
from tempfile import TemporaryFile

from typing import Annotated, List, Optional
import httpx
from msgspec import field
import msgspec
from orchard.libs.bunny_storage.bunny_storage import BunnyStorage
from orchard.libs.melite.base import JSON, MeliteStruct
from orchard.libs.vitals.pydantic_model import VitalsLevelBase
from orchard.projects.v1.core.auth import AssetURLScope, OrchardAuthScopes, make_token_now
from orchard.projects.v1.core.config import config
from orchard.libs.vitals import analyze
from orchard.projects.v1.models.publishers import Publisher
from orchard.projects.v1.models.users import User


class RDLevel(MeliteStruct):
    """
    We're repeating fields from VitalsLevelBase
    because there are fields that we don't want to store for now
    such as the colortoken stuff
    """
    table_name = "rdlevel"

    id: str
    artist: str
    artist_tokens: Annotated[List[str], JSON]
    song: str
    seizure_warning: bool
    description: str
    hue: float
    authors: Annotated[List[str], JSON]
    authors_raw: str
    max_bpm: float
    min_bpm: float
    difficulty: int
    single_player: bool
    two_player: bool
    last_updated: datetime
    tags: Annotated[List[str], JSON]
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

    image: str  # url
    thumb: str  # url
    icon: Optional[str]
    url: str

    # e.g. localised title if song is CJK
    song_alt: str

    # who uploaded the level.
    # authors is just a list of strings which may not actually be a user.
    uploader: User
    publisher: Publisher

    uploaded: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    approval: int = 0


class RDPrefillResult(VitalsLevelBase, kw_only=True):
    image: str
    thumb: str
    url: str
    icon: Optional[str] = None
    song_ct: msgspec.UnsetType = msgspec.UNSET
    description_ct: msgspec.UnsetType = msgspec.UNSET

class RDPrefillResultWithToken(msgspec.Struct, kw_only=True):
    result: RDPrefillResult
    signed_token: str

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

            payload = {
                **msgspec.structs.asdict(level),
                "thumb": thumb,
                "image": image,
                "icon": icon,
                "url": url
            }
            to_send = msgspec.convert(payload, RDPrefillResult)
            asset_token_scopes = msgspec.convert(payload, AssetURLScope)

            asset_token = make_token_now(
                scopes=OrchardAuthScopes(
                    Publisher_prefill=asset_token_scopes
                ),
                exp_time=timedelta(days=1)
            )
            return RDPrefillResultWithToken(result=to_send, signed_token=asset_token)