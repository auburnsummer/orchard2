from orchard.projects.v1.core.auth import (
    OrchardAuthToken,
    parse_token_from_request,
    InvalidToken,
    requires_scopes
)
from orchard.projects.v1.models.users import (
    User,
    get_all_users,
    add_user,
    inject_user
)
from pydantic import BaseModel

from starlette.responses import JSONResponse
from starlette.requests import Request

@inject_user
async def me_handler(request: Request):
    user: User = request.state.user
    return JSONResponse(user.model_dump(mode="json"))