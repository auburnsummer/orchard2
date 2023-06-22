from orchard.projects.v1.models.users import (
    get_all_users,
    add_user
)
from pydantic import BaseModel

from starlette.responses import JSONResponse


async def list_users_handler(request):
    users = await get_all_users()
    return JSONResponse([user.to_dict() for user in users])


class AddUserHandlerArgs(BaseModel):
    name: str

async def add_user_handler(request):
    data = AddUserHandlerArgs(**await request.json())
    user = await add_user(data.name)
    return JSONResponse(user.to_dict())