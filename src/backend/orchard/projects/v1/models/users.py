"""
A User is an individual in the site.

Users are expected to have at least one Credential attached to them. This allows them to login with that Credential.

For the initial scope, the only Credential planned is Discord login.
"""
from __future__ import annotations
from datetime import datetime

from functools import wraps
from orchard.projects.v1.core.auth import requires_scopes, OrchardAuthToken
from orchard.projects.v1.core.exceptions import UserDoesNotExist, UserIsLoggedOut
from starlette.requests import Request
from .metadata import engine, metadata
from uuid import uuid4

import sqlalchemy as sa

import msgspec

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

class User(msgspec.Struct):
    id: str
    name: str
    cutoff: datetime = datetime.utcfromtimestamp(0)
    avatar_url: Optional[str] = None

    def to_dict(self):
        return msgspec.structs.asdict(self)



class EditUser(msgspec.Struct):
    name: Optional[str] = None
    cutoff: Optional[datetime] = None
    avatar_url: Optional[str] = None

    def to_dict(self):
        payload = msgspec.structs.asdict(self)
        filtered_payload = {k: v for k, v in payload.items() if v is not None}
        return filtered_payload




async def get_user_by_id(id: str):
    async with engine.begin() as conn:
        query = users.select().where(users.c.id == id)
        result = (await conn.execute(query)).first()

    if result:
        return msgspec.convert(result._mapping, User)
    else:
        raise UserDoesNotExist(user_id=id)


async def get_user_by_discord_credential(cred: DiscordCredential):
    id = cred.user_id
    return await get_user_by_id(id)


async def get_all_users():
    async with engine.begin() as conn:
        query = users.select()
        results = (await conn.execute(query)).all()

    return [msgspec.convert(result._mapping, User) for result in results]


async def add_user(name: str):
    new_id = uuid4().hex
    user = User(id=new_id, name=name)

    async with engine.begin() as conn:
        query = users.insert().values(user.to_dict())
        await conn.execute(query)

    resultant_user = await get_user_by_id(new_id)
    return resultant_user


async def update_user(user_id: str, data: EditUser):
    values = data.to_dict()

    async with engine.begin() as conn:
        query = users.update().where(users.c.id == user_id).values(**values)
        await conn.execute(query)
        
    resultant_user = await get_user_by_id(user_id)
    return resultant_user



def inject_user(func):
    """
    Decorator. Places the logged-in user as request.state.user.

    Exits early if there is anything wrong with the token.
    """
    @wraps(func)
    @requires_scopes({"User_all"})
    async def inner(request: Request):
        token: OrchardAuthToken = request.state.token
        user_id = token.User_all

        # requires_scopes will already make sure user is defined.
        assert user_id is not None
        
        user = await get_user_by_id(user_id)
        if token.iat < user.cutoff:
            raise UserIsLoggedOut(user_id=user_id)
        request.state.user = user
        return await func(request)
    return inner