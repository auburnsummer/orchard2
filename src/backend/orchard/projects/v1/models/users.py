"""
A User is an individual in the site.

Users are expected to have at least one Credential attached to them.
This allows them to login with that Credential.

For the initial scope, the only Credential planned is Discord login.
"""
from __future__ import annotations
from functools import wraps
from typing import Optional, Self

from datetime import datetime, timezone
from orchard.libs.utils.gen_id import IDType, gen_id
from orchard.projects.v1.core.exceptions import UserDoesNotExist, UserIsLoggedOut
from orchard.projects.v1.models.engine import select, insert
from starlette.requests import Request

from orchard.libs.melite.base import MeliteStruct
from orchard.projects.v1.core.auth import requires_scopes, OrchardAuthToken


class User(MeliteStruct):
    table_name = "user"
    id: str
    name: str
    cutoff: datetime = datetime.fromtimestamp(0, tz=timezone.utc)
    avatar_url: Optional[str] = None

    @staticmethod
    def create(name: str) -> User:
        "Creates a new user with the specified name and inserts that user into the db."
        new_user = User(
            id=gen_id(IDType.USER),
            name=name
        )
        insert(new_user)
        return new_user

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

        # requires_scopes will already make sure user is defined, this is for typing.
        # todo: figure out how to type requires_scopes
        assert user_id is not None

        user = select(User).by_id(user_id)
        if not user:
            raise UserDoesNotExist(user_id=user_id)
        
        if token.iat < user.cutoff:
            raise UserIsLoggedOut(user_id=user_id)
        request.state.user = user
        return await func(request)
    return inner
