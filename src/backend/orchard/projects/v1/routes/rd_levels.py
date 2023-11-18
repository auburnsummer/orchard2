import msgspec
from orchard.libs.utils.gen_id import IDType, gen_id
from orchard.projects.v1.core.auth import OrchardAuthToken, requires_scopes
from orchard.projects.v1.core.exceptions import LevelAddURLMismatch, PublisherDoesNotExist, UserDoesNotExist
from orchard.projects.v1.core.wrapper import msgspec_return, parse_body_as
from orchard.projects.v1.models.engine import insert, select
from orchard.projects.v1.models.publishers import Publisher
from orchard.projects.v1.models.rd_levels import RDLevel, RDPrefillResult, run_prefill
from orchard.projects.v1.models.users import User, inject_user

from starlette.requests import Request


@msgspec_return(200)
@requires_scopes({"Publisher_add"})
async def prefill_handler(request: Request):
    token: OrchardAuthToken = request.state.token
    assert token.Publisher_add is not None  # requires_scopes should ensure this already.

    source_url = token.Publisher_add.url

    prefill_result = await run_prefill(source_url)
    return prefill_result

class RDPrefillResultTruncated(RDPrefillResult, kw_only=True):
    image: msgspec.UnsetType = msgspec.UNSET
    thumb: msgspec.UnsetType = msgspec.UNSET
    url: msgspec.UnsetType = msgspec.UNSET
    icon: msgspec.UnsetType = msgspec.UNSET
    sha1: msgspec.UnsetType = msgspec.UNSET
    rdlevel_sha1: msgspec.UnsetType = msgspec.UNSET
    is_animated: msgspec.UnsetType = msgspec.UNSET

    song_alt: str

class AddRdLevelHandlerArgs(msgspec.Struct):
    level: RDPrefillResultTruncated

class AddRdlevelResponse(msgspec.Struct):
    level: RDLevel

@msgspec_return(201)
@parse_body_as(AddRdLevelHandlerArgs)
@requires_scopes({"Publisher_add", "Publisher_prefill"})
async def add_rd_level_handler(request: Request):
    token: OrchardAuthToken = request.state.token
    body: AddRdLevelHandlerArgs = request.state.body

    assert token.Publisher_add is not None
    assert token.Publisher_prefill is not None

    if token.Publisher_add.url != token.Publisher_prefill.url:
        raise LevelAddURLMismatch(url1=token.Publisher_add.url, url2=token.Publisher_prefill.url)

    uploader = select(User).by_id(token.Publisher_add.user_id)
    if not uploader:
        raise UserDoesNotExist(user_id=token.Publisher_add.user_id)

    publisher = select(Publisher).by_id(token.Publisher_add.publisher_id)
    if not publisher:
        raise PublisherDoesNotExist(publisher_id=token.Publisher_add.publisher_id)

    payload = {
        **msgspec.structs.asdict(body.level),
        **msgspec.structs.asdict(token.Publisher_prefill),
        "uploader": uploader,
        "publisher": publisher,
        "id": gen_id(IDType.RD_LEVEL)
    }

    level = msgspec.convert(payload, RDLevel, strict=False)
    insert(level, recurse=False)  # user, publisher already exist.

    return AddRdlevelResponse(level=level)