"""
A Level is a single playable level backed by an rdzip file.

All levels belong to a user and a publisher.
"""

from __future__ import annotations
import asyncio
from datetime import datetime, timedelta, timezone
from io import BytesIO
from tempfile import TemporaryFile
from textwrap import dedent

from typing import Annotated, List, Optional, Tuple
import httpx
from msgspec import field
import msgspec
from orchard.libs.bunny_storage.bunny_storage import BunnyStorage
from orchard.libs.melite.base import JSON, MeliteStruct
from orchard.libs.vitals.msgspec_schema import VitalsLevelBase
from orchard.projects.v1.core.auth import OrchardAuthScopes, PublisherAddAssetsScope, PublisherRDPrefillScope, make_token_now
from orchard.projects.v1.core.config import config
from orchard.libs.vitals import analyze
from orchard.projects.v1.models.engine import select
from orchard.projects.v1.models.publishers import Publisher
from orchard.projects.v1.models.users import User

from loguru import logger

class FloatRange(msgspec.Struct):
    max: float
    min: float

class IntRange(msgspec.Struct):
    max: int
    min: int
    

class RDSearchParams(msgspec.Struct):
    q: Optional[str] = None
    tags: List[str] = []
    artists: List[str] = []
    authors: List[str] = []
    min_bpm: Optional[float] = None
    max_bpm: Optional[float] = None
    min_difficulty: Optional[int] = None
    max_difficulty: Optional[int] = None
    single_player: Optional[bool] = None
    two_player: Optional[bool] = None
    has_classics: Optional[bool] = None
    has_oneshots: Optional[bool] = None
    has_squareshots: Optional[bool] = None
    has_freezeshots: Optional[bool] = None
    has_freetimes: Optional[bool] = None
    has_holds: Optional[bool] = None
    has_skipshots: Optional[bool] = None
    has_window_dance: Optional[bool] = None

    uploader: Optional[str] = None
    publisher: Optional[str] = None

    min_approval: Optional[int] = None
    max_approval: Optional[int] = None


class RDLevel(MeliteStruct):
    """
    We're repeating fields from VitalsLevelBase
    because there may be fields in there we don't want to store
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

    @staticmethod
    def by_sha1(sha1: str) -> Optional[RDLevel]:
        cursor = select(RDLevel).cursor()
        q = f"""
--sql
SELECT * FROM {RDLevel.table_name}
WHERE sha1 = ?
"""
        cursor.execute(q, [sha1])
        return next(cursor, None)

    @staticmethod
    def query(params: RDSearchParams) -> List[RDLevel]:
        # build a query...
        the_query = "SELECT * FROM rdlevel"
        parameters = []

        # q, we need to join so we can order by rank later
        if params.q:
            the_query += dedent("""
                INNER JOIN (
                    SELECT id, rank FROM rdlevel_search
                        WHERE rdlevel_search MATCH ?
                ) AS search ON search.id = rdlevel.id
            """)
            parameters.append(params.q)

        # so we don't have to think about if there's at least one WHERE. this is compiled out by sqlite planner.
        the_query += "\nWHERE TRUE"

        # parameters involving a list of things the levels have to meet.
        # there are subtables pre-prepared for this, so we don't need to use json_each here.
        set_parameters: List[Tuple[List[str], str, str]] = [
            (params.tags, "rdlevel_tag", "tag"),
            (params.artists, "rdlevel_artist", "artist"),
            (params.authors, "rdlevel_author", "author")
        ]

        for wanted, subtable, param_name in set_parameters:
            if len(wanted) == 0:
                continue
            placeholders = ','.join(["?"] * len(wanted))
            the_query += dedent(f"""
                AND rdlevel.id IN (
                    SELECT rdlevel FROM {subtable}
                        WHERE {param_name} IN ({placeholders})
                    GROUP BY rdlevel
                    HAVING COUNT(DISTINCT {param_name}) = ?
                )
            """)
            parameters.extend(wanted)
            parameters.append(len(wanted))

        # parameters that are simply a check of equality against the given value.
        value_params: List[Tuple[Optional[bool | str | int], str]] = [
            (params.single_player, "single_player"),
            (params.two_player, "two_player"),
            (params.has_classics, "has_classics"),
            (params.has_oneshots, "has_oneshots"),
            (params.has_squareshots, "has_squareshots"),
            (params.has_freezeshots, "has_freezeshots"),
            (params.has_freetimes, "has_freetimes"),
            (params.has_holds, "has_holds"),
            (params.has_skipshots, "has_skipshots"),
            (params.has_window_dance, "has_window_dance"),
            (params.uploader, "uploader"),
            (params.publisher, "publisher")
        ]

        for wanted, param_name in value_params:
            if wanted is None:
                continue

            the_query += dedent("""
                AND rdlevel.{param_name} = ?                    
            """)
            parameters.append(wanted)

        # parameters where a single value needs to be within a specified range.
        range_params: List[Tuple[Optional[int | float], Optional[int | float], str]] = [
            (params.min_approval, params.max_approval, "approval"),
            (params.min_difficulty, params.max_difficulty, "difficulty")
        ]

        for min_value, max_value, param_name in range_params:
            if min_value:
                the_query += dedent(f"""
                    AND rdlevel.{param_name} >= ?                 
                """)
                parameters.append(min_value)
            if max_value:
                the_query += dedent(f"""
                    AND rdlevel.{param_name} <= ?            
                """)
                parameters.append(max_value)

        # bpm is special.
        if params.min_bpm:
            the_query += dedent(f"""
                AND rdlevel.min_bpm >= ?     
            """)
            parameters.append(params.min_bpm)

        if params.max_bpm:
            the_query += dedent(f"""
                AND rdlevel.max_bpm <= ?                    
            """)
            parameters.append(params.max_bpm)

        if params.q:
            the_query += dedent("""
                ORDER BY rank
            """)
        else:
            the_query += dedent("""
                ORDER BY last_updated DESC                    
            """)
        
        logger.info(the_query)
        cursor = select(RDLevel).cursor()
        cursor.execute(the_query, parameters)
        return list(cursor)



class RDPrefillResult(VitalsLevelBase, kw_only=True):
    image: str
    thumb: str
    url: str
    icon: Optional[str] = None

class RDPrefillResultWithToken(msgspec.Struct, kw_only=True):
    result: RDPrefillResult
    signed_token: str

async def run_prefill(scope: PublisherRDPrefillScope):
    source_url = scope.url
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

            level_dict = msgspec.structs.asdict(level)

            asset_urls = {
                "thumb": thumb,
                "image": image,
                "icon": icon,
                "url": url
            }

            payload = {
                **level_dict,
                **asset_urls
            }
            to_send = msgspec.convert(payload, RDPrefillResult)

            publisher_assets_scope = {
                **payload,
                "link_id": scope.link_id
            }

            publisher_assets_scope = msgspec.convert(publisher_assets_scope, PublisherAddAssetsScope)

            asset_token = make_token_now(
                scopes=OrchardAuthScopes(
                    Publisher_rdadd=publisher_assets_scope
                ),
                exp_time=timedelta(days=1)
            )
            return RDPrefillResultWithToken(result=to_send, signed_token=asset_token)