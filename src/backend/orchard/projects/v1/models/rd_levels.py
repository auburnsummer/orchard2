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
from orchard.projects.v1.models.engine import select, temporary_table, make_cursor
from orchard.projects.v1.models.publishers import Publisher
from orchard.projects.v1.models.users import User

from loguru import logger

class FloatRange(msgspec.Struct):
    max: float
    min: float

class IntRange(msgspec.Struct):
    max: int
    min: int

MAX_FACETS = 100    

class RDSearchParams(msgspec.Struct):
    q: Optional[str] = None
    tags: List[str] = []
    artists: List[str] = []
    authors: List[str] = []
    min_bpm: Optional[float] = None
    max_bpm: Optional[float] = None
    difficulty: Optional[List[int]] = None
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

    offset: Annotated[int, msgspec.Meta(ge=0)] = 0
    limit: Annotated[int, msgspec.Meta(gt=0, le=100)] = 50

class StrFacetValue(MeliteStruct):
    "Not actually table-backed, but we do select a thing in this shape eventually. todo: a better way to handle this sort of thing"
    table_name = "_"
    value: str
    count: int 

class IntFacetValue(MeliteStruct):
    "Not actually table-backed, but we do select a thing in this shape eventually. todo: a better way to handle this sort of thing"
    table_name = "_"
    value: int
    count: int 


class RDQueryResult(msgspec.Struct):
    levels: List[RDLevel]
    tags: List[StrFacetValue]
    artists: List[StrFacetValue]
    authors: List[StrFacetValue]
    difficulties: List[IntFacetValue]

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
    def query(params: RDSearchParams):
        with temporary_table() as temp:

            # build a query. this first query is all levels that match the requirements.
            # we need to get all levels regardless of the LIMIT set, because otherwise we cannot
            # accurately calculate facets.
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

            # difficulty
            if params.difficulty:
                placeholders = ','.join(["?"] * len(params.difficulty))
                the_query += dedent(f"""
                    AND rdlevel.difficulty IN ({placeholders})               
                """)
                parameters.extend(params.difficulty)

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

            # select and save it in our temp database we made.
            make_cursor().execute(f"CREATE TABLE \"{temp}\".\"scratch\" AS {the_query}", parameters)


            # now select from it.
            query2 = f"SELECT * FROM \"{temp}\".\"scratch\" LIMIT ? OFFSET ?"
            params2 = [params.limit, params.offset]
            
            cursor = select(RDLevel).cursor()
            cursor.execute(query2, params2)

            levels = list(cursor)

            # faceting! tags
            sfacet_cursor = select(StrFacetValue).cursor()
            query3 = dedent(f"""
                SELECT tag AS value, COUNT(*) as count FROM rdlevel_tag WHERE rdlevel in (
                    SELECT id FROM \"{temp}\".\"scratch\"
                )
                GROUP BY tag
                ORDER BY count DESC
                LIMIT {MAX_FACETS}
            """)
            sfacet_cursor.execute(query3)
            tags_facet = list(sfacet_cursor)
            # artists
            query4 = dedent(f"""
                SELECT artist AS value, COUNT(*) as count FROM rdlevel_artist WHERE rdlevel in (
                    SELECT id FROM \"{temp}\".\"scratch\"
                )
                GROUP BY artist
                ORDER BY count DESC
                LIMIT {MAX_FACETS}
            """)
            sfacet_cursor.execute(query4)
            artists_facet = list(sfacet_cursor)

            # authors
            query5 = dedent(f"""
                SELECT author AS value, COUNT(*) as count FROM rdlevel_author WHERE rdlevel in (
                    SELECT id FROM \"{temp}\".\"scratch\"
                )
                GROUP BY author
                ORDER BY count DESC
                LIMIT {MAX_FACETS}
            """)
            sfacet_cursor.execute(query5)
            authors_facet = list(sfacet_cursor)

            # difficulty
            query6 = dedent(f"""
                SELECT difficulty AS value, COUNT(*) as count FROM \"{temp}\".\"scratch\"
                GROUP BY difficulty
                ORDER BY difficulty ASC
            """)
            ifacet_cursor = select(IntFacetValue).cursor()
            ifacet_cursor.execute(query6)
            difficulty_facet = list(ifacet_cursor)

            return RDQueryResult(
                levels=levels,
                tags=tags_facet,
                artists=artists_facet,
                authors=authors_facet,
                difficulties=difficulty_facet
            )


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