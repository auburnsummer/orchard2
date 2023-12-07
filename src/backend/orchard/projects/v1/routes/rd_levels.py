from typing import List
import msgspec
from orchard.libs.utils.gen_id import IDType, gen_id
from orchard.libs.vitals.msgspec_schema import VitalsLevelBaseMutable
from orchard.projects.v1.core.auth import OrchardAuthToken, requires_scopes
from orchard.projects.v1.core.exceptions import LinkedTokensIDMismatch, PublisherDoesNotExist, RDLevelAlreadyExists, UserDoesNotExist
from orchard.projects.v1.core.wrapper import msgspec_return, parse_body_as, parse_qs_as
from orchard.projects.v1.models.engine import insert, select
from orchard.projects.v1.models.publishers import Publisher
from orchard.projects.v1.models.rd_levels import RDLevel, RDSearchParams, run_prefill
from orchard.projects.v1.models.users import User

from starlette.requests import Request


@msgspec_return(200)
@requires_scopes({"Publisher_rdprefill"})
async def prefill_handler(request: Request):
    token: OrchardAuthToken = request.state.token
    assert token.Publisher_rdprefill is not None  # requires_scopes should ensure this already.

    prefill_result = await run_prefill(token.Publisher_rdprefill)
    existing_level = RDLevel.by_sha1(prefill_result.result.sha1)
    if existing_level is not None:
        raise RDLevelAlreadyExists(level_id=existing_level.id, sha1=prefill_result.result.sha1)
    return prefill_result

class AddRDLevelPayload(VitalsLevelBaseMutable, kw_only=True):
    song_alt: str

class AddRDLevelHandlerArgs(msgspec.Struct):
    level: AddRDLevelPayload

class AddRdlevelResponse(msgspec.Struct):
    level: RDLevel

@msgspec_return(201)
@parse_body_as(AddRDLevelHandlerArgs)
@requires_scopes({"Publisher_rdadd", "Publisher_rdprefill"})
async def add_rd_level_handler(request: Request):
    token: OrchardAuthToken = request.state.token
    body: AddRDLevelHandlerArgs = request.state.body

    assert token.Publisher_rdadd is not None
    assert token.Publisher_rdprefill is not None

    # the link_id of both tokens should match.
    if token.Publisher_rdadd.link_id != token.Publisher_rdprefill.link_id:
        raise LinkedTokensIDMismatch(id1=token.Publisher_rdadd.link_id, id2=token.Publisher_rdprefill.link_id, context="adding rd level")

    # the allowed user + publisher is encoded in the prefill token.
    uploader = select(User).by_id(token.Publisher_rdprefill.user_id)
    if not uploader:
        raise UserDoesNotExist(user_id=token.Publisher_rdprefill.user_id)

    publisher = select(Publisher).by_id(token.Publisher_rdprefill.publisher_id)
    if not publisher:
        raise PublisherDoesNotExist(publisher_id=token.Publisher_rdprefill.publisher_id)

    
    payload = {
        **msgspec.structs.asdict(body.level),
        **msgspec.structs.asdict(token.Publisher_rdadd),
        "uploader": uploader,
        "publisher": publisher,
        "id": gen_id(IDType.RD_LEVEL)
    }

    level = msgspec.convert(payload, RDLevel, strict=False)
    insert(level, recurse=False)  # user, publisher already exist.

    return AddRdlevelResponse(level=level)

class SearchRDLevelsResponse(msgspec.Struct):
    levels: List[RDLevel]

@msgspec_return(200)
@parse_qs_as(RDSearchParams)
async def search_rd_levels_handler(request: Request):
    body: RDSearchParams = request.state.query

    results = RDLevel.query(body)
    
    return results