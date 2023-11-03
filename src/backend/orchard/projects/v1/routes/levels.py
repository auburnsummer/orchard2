from orchard.projects.v1.core.auth import OrchardAuthToken, requires_scopes
from orchard.projects.v1.core.wrapper import msgspec_return
from orchard.projects.v1.models.levels import run_prefill
from orchard.projects.v1.models.users import inject_user

from starlette.requests import Request


@msgspec_return(200)
@inject_user
@requires_scopes({"Publisher_add"})
async def prefill_handler(request: Request):
    token: OrchardAuthToken = request.state.token
    assert token.Publisher_add is not None  # requires_scopes should ensure this already.

    source_url = token.Publisher_add.url

    prefill_result = await run_prefill(source_url)
    return prefill_result


@msgspec_return(201)
@inject_user
@requires_scopes({"Publisher_add", "Publisher_assets"})
async def add_level_handler(request: Request):
    pass