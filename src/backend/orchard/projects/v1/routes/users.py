from orchard.projects.v1.core.wrapper import msgspec_return
from orchard.projects.v1.models.users import (
    EditUser,
    User,
    inject_user,
    update_user
)
from starlette.responses import Response
from starlette.requests import Request

from datetime import datetime


@msgspec_return(200)
@inject_user
async def me_handler(request: Request):
    user: User = request.state.user
    return user


@inject_user
async def logout_handler(request: Request):
    """
    Logout the user. This sets the cutoff date to the current time, which invalidates tokens
    issued before the cutoff. For us, this means we can't log out individual clients of the
    same user. I don't think this should be too much of an issue.
    """
    user: User = request.state.user
    _ = await update_user(user.id, EditUser(cutoff=datetime.utcnow()))

    return Response(status_code=204)