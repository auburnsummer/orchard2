"""
A User is an individual in the site.

Users are expected to have at least one Credential attached to them. This allows them to login with that Credential.

For the initial scope, the only Credential planned is Discord login.
"""
from __future__ import annotations
from datetime import datetime

from functools import wraps
from orchard.libs.utils.dict_filter import without_keys
from orchard.projects.v1.core.auth import requires_scopes, OrchardAuthToken
from pydantic import BaseModel, Field
from starlette.requests import Request
from starlette.responses import JSONResponse
from .metadata import database, metadata
from uuid import uuid4

import sqlalchemy as sa

from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from orchard.projects.v1.models.credentials import DiscordCredential


users = sa.Table(
    "users",
    metadata,
    sa.Column("id", sa.String, primary_key=True),
    sa.Column("name", sa.String, nullable=False),
    sa.Column("cutoff", sa.DateTime, nullable=False),
    sa.Column("avatar_url", sa.String, nullable=True)
)

class User(BaseModel):
    id: str
    name: str
    cutoff: datetime = Field(default=datetime.utcfromtimestamp(0))
    avatar_url: Optional[str] = Field(default=None)

    def to_dict(self):
        return self.model_dump()


class EditUser(BaseModel):
    name: Optional[str] = Field(default=None)
    cutoff: Optional[datetime] = Field(default=None)
    avatar_url: Optional[str] = Field(default=None)


class UserNotFoundException(Exception):
    pass


class UserLoggedOutException(Exception):
    pass


async def get_user_by_id(id: str):
    query = users.select().where(users.c.id == id)
    result = await database.fetch_one(query)
    if result:
        return User(**result)
    else:
        raise UserNotFoundException(f"The user with id {id} was not found.")


async def get_user_by_discord_credential(cred: DiscordCredential):
    id = cred.user_id
    return await get_user_by_id(id)


async def get_all_users():
    query = users.select()
    results = await database.fetch_all(query)
    return [User(**result) for result in results]


async def add_user(name: str):
    new_id = uuid4().hex
    user = User(id=new_id, name=name)
    query = users.insert().values(**user.model_dump(mode="python"))
    await database.execute(query)
    resultant_user = await get_user_by_id(new_id)
    return resultant_user


async def update_user(user_id: str, data: EditUser):
    values = data.model_dump(mode="python", exclude_unset=True, exclude_none=True)
    query = users.update().where(users.c.id == user_id).values(**values)
    await database.execute(query)
    resultant_user = await get_user_by_id(user_id)
    return resultant_user



def inject_user(func):
    @wraps(func)
    @requires_scopes({"user"})
    async def inner(request: Request):
        token: OrchardAuthToken = request.state.token
        user_id: str = token.user
        try:
            user = await get_user_by_id(user_id)
            if token.iat < user.cutoff:
                raise UserLoggedOutException()
            request.state.user = user
            return await func(request)
        except UserNotFoundException:
            content = {
                "error": f"user with id {user_id} does not exist."
            }
            return JSONResponse(status_code=401, content=content)
        except UserLoggedOutException:
            content = {
                "error": f"user with id {user_id} has been logged out."
            }
            return JSONResponse(status_code=401, content=content)
    return inner