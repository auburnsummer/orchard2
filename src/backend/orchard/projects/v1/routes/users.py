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


async def list_users_handler(request):
    users = await get_all_users()
    return JSONResponse([user.to_dict() for user in users])


class AddUserHandlerArgs(BaseModel):
    name: str


async def add_user_handler(request: Request):
    data = AddUserHandlerArgs(**await request.json())
    user = await add_user(data.name)
    return JSONResponse(user.to_dict())


@inject_user
async def me_handler(request: Request):
    user: User = request.state.user
    return JSONResponse(user.model_dump(mode="json"))
    # try:
    #     parsed_token = parse_token_from_request(request)
    # except InvalidToken as exc:
    #     return JSONResponse(status_code=401, content={"error": str(exc)})

    # return JSONResponse(parsed_token.model_dump(mode="json"))