"""
Auth tokens are PASETO tokens encoding the user.
"""
from __future__ import annotations

from base64 import b64decode
import json
from orchard.projects.v1.core.exceptions import AuthorizationHeaderInvalid, AuthorizationHeaderTokenTypeIsNotBearer, MissingAuthorizationHeader, MissingScopes, NoAuthorizationHeaderTokenType

from .config import config

import pyseto

from datetime import datetime, timedelta, timezone
from functools import wraps
from typing import List, Optional, Set

from starlette.requests import Request

import msgspec


class PublisherAddScope(msgspec.Struct):
    publisher_id: str
    user_id: str
    url: str

class AssetURLScope(msgspec.Struct, kw_only=True):
    """
    indicates that these image / thumb / icon combo is allowed to be submitted with this url
    """
    image: str
    thumb: str
    url: str
    icon: Optional[str] = None
    sha1: str
    rdlevel_sha1: str
 
class OrchardAuthScopes(msgspec.Struct, kw_only=True):
    "The keys and value types that a token can have."
    User_all: Optional[str] = None  # the bearer is this user.
    Admin_all: Optional[bool] = None  # if true, bearer is an admin.
    DiscordGuild_register: Optional[str] = None  # this discord guild can be used to register.
    Publisher_identify: Optional[str] = None  # this token yields this publisher with the /identify endpoint.
    Publisher_add: Optional[PublisherAddScope] = None  # this specific publisher id and url can be added
    Publisher_prefill: Optional[AssetURLScope] = None

class OrchardAuthToken(OrchardAuthScopes):
    iat: datetime
    exp: datetime


def combine_tokens(tokens: List[OrchardAuthToken]):
    final_iat = max(t.iat for t in tokens)
    final_exp = min(t.exp for t in tokens)
    token_args = {}
    for token in tokens:
        for field in msgspec.structs.fields(token):
            value = getattr(token, field.name)
            if value:
                token_args[field.name] = getattr(token, field.name)

    token_args["iat"] = final_iat
    token_args["exp"] = final_exp
    token = OrchardAuthToken(**token_args)

    return token

paseto_key = pyseto.Key.new(version=4, purpose="local", key=b64decode(config().PASETO_KEY_BASE64.get_secret_value()))

"""
Token generation:
from orchard.projects.v1.core.auth import OrchardAuthToken, token_to_paseto
from datetime import datetime, timedelta

token = OrchardAuthToken(iat=datetime.now(timezone.utc), exp=datetime.now(timezone.utc) + timedelta(hours=1)) # other args as reqd
paseto = token_to_paseto(token)
"""

def make_token_now(scopes: OrchardAuthScopes, exp_time: timedelta):
    iat = datetime.now(timezone.utc)
    exp = iat + exp_time
    token_args = {
        "iat": iat,
        "exp": exp
    }
    for field in msgspec.structs.fields(scopes):
        token_args[field.name] = getattr(scopes, field.name)
    token = OrchardAuthToken(**token_args)
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

    pasetos = auth_header.split(",")

    parsed_tokens = []
    for paseto in pasetos:
        try:
            auth_type, string_token = paseto.split(" ")
        except ValueError:
            raise NoAuthorizationHeaderTokenType()

        if auth_type.lower() != "bearer":
            raise AuthorizationHeaderTokenTypeIsNotBearer()

        try:
            parsed_token = paseto_to_token(string_token)
            parsed_tokens.append(parsed_token)
        except (ValueError, pyseto.DecryptError, pyseto.VerifyError) as exc:
            raise AuthorizationHeaderInvalid(message=str(exc))  
    
    return combine_tokens(parsed_tokens)


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
                if getattr(parsed_token, scope, None) is None:
                    raise MissingScopes(scope=scope)
            else:
                request.state.token = parsed_token
                return await func(request)
        return inner
    return decorator
