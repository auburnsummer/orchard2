"""
Auth tokens are PASETO tokens encoding the user.
"""

from base64 import b64decode
import json
from orchard.projects.v1.core.exceptions import AuthorizationHeaderInvalid, AuthorizationHeaderTokenTypeIsNotBearer, MissingAuthorizationHeader, MissingScopes, NoAuthorizationHeaderTokenType

from pyseto.exceptions import VerifyError
from .config import config

import pyseto

from datetime import datetime, timedelta
from functools import wraps
from typing import Callable, Optional, Set, Any, TypedDict

from starlette.requests import Request

import msgspec

class PublisherScope(msgspec.Struct):
    publisher_id: str
    action: str
 
class OrchardAuthScopes(msgspec.Struct, kw_only=True):
    "The keys and value types that a token can have."
    user: Optional[str] = None  # the bearer is this user.
    admin: Optional[bool] = None  # if true, bearer is an admin.
    publisher: Optional[PublisherScope] = None  # the specific action is approved by this publisher.
    discord_guild: Optional[str] = None  # the bearer is a representative of this discord guild.

class OrchardAuthToken(OrchardAuthScopes):
    iat: datetime
    exp: datetime


paseto_key = pyseto.Key.new(version=4, purpose="local", key=b64decode(config().PASETO_KEY_BASE64.get_secret_value()))

"""
Token generation:
from orchard.projects.v1.core.auth import OrchardAuthToken, token_to_paseto
from datetime import datetime, timedelta

token = OrchardAuthToken(iat=datetime.now(), exp=datetime.now() + timedelta(hours=1)) # other args as reqd
paseto = token_to_paseto(token)
"""

def make_token_now(scopes: OrchardAuthScopes, exp_time: timedelta):
    iat = datetime.now()
    exp = iat + exp_time
    token = OrchardAuthToken(
        iat=iat,
        exp=exp,
        user=scopes.user,
        admin=scopes.admin,
        publisher=scopes.publisher,
        discord_guild=scopes.discord_guild
    )
    return token_to_paseto(token)


def _token_to_paseto(token: OrchardAuthToken):
    payload = msgspec.json.encode(token)
    encoded_token = pyseto.encode(
        key=paseto_key,
        payload=payload
    )
    return encoded_token.decode('utf-8')


def token_to_paseto(token: OrchardAuthToken):
    return _token_to_paseto(token)


def paseto_to_token(paseto: str):
    token = pyseto.decode(
        keys=paseto_key,
        token=paseto,
        deserializer=json
    )
    return msgspec.convert(token.payload, OrchardAuthToken)
 

class InvalidToken(Exception):
    pass


def parse_token_from_request(request: Request):
    try:
        auth_header = request.headers["Authorization"]
    except KeyError:
        raise MissingAuthorizationHeader()
 
    try:
        auth_type, token = auth_header.split(" ")
    except ValueError:
        raise NoAuthorizationHeaderTokenType()

    if auth_type.lower() != "bearer":
        raise AuthorizationHeaderTokenTypeIsNotBearer()

    try:
        return paseto_to_token(token)
    except (ValueError, pyseto.DecryptError, pyseto.VerifyError) as exc:
        raise AuthorizationHeaderInvalid(message=str(exc))


def requires_scopes(scopes: Set[str]):
    """
    Decorator. Give it a set of scopes, and it will ensure those scopes are
    defined in the token.

    NB: This _does not_ check the value of the scope, just that it's defined.
    Typically, we will have a specialized version of this decorator, such as
    @inject_user and @requires_admin for specific routes, rather than using
    @requires_scopes directly.

    Order: This can return OrchardExceptions, so use with msgspec_return is recommended.
    Put it before (below) msgspec_return. 
    """
    def decorator(func):
        @wraps(func)
        async def inner(request: Request):
            parsed_token = parse_token_from_request(request)
            for scope in scopes:
                if getattr(parsed_token, scope) is None:
                    raise MissingScopes(scope=scope)
            else:
                request.state.token = parsed_token
                return await func(request)
        return inner
    return decorator
