"""
Auth tokens are PASETO tokens encoding the user.
"""

from base64 import b64decode
import json

from pyseto.exceptions import VerifyError
from .config import config

import pyseto

from datetime import datetime, timedelta
from functools import wraps
from typing import Callable, Optional, Set, Any

from starlette.requests import Request
from starlette.responses import JSONResponse

import msgspec

 

class OrchardAuthScopes(msgspec.Struct, kw_only=True):
    user: Optional[str] = None

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
        user=scopes.user
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
        raise InvalidToken("No Authorization header.")

    try:
        auth_type, token = auth_header.split(" ")
    except ValueError:
        raise InvalidToken("No token type.")

    if auth_type.lower() != "bearer":
        raise InvalidToken("Token type should be Bearer.")

    try:
        return paseto_to_token(token)
    except ValueError as exc:
        raise InvalidToken(str(exc))


def requires_scopes(scopes: Set[str]):
    def decorator(func):
        @wraps(func)
        async def inner(request: Request):
            try:
                parsed_token = parse_token_from_request(request)
                for scope in scopes:
                    if getattr(parsed_token, scope) is None:
                        raise InvalidToken(f"Token lacks the required scope: {scope}")
                else:
                    request.state.token = parsed_token
                    return await func(request)
            except InvalidToken as exc:
                return JSONResponse(status_code=401, content={"error": str(exc)})
            except VerifyError as exc:
                return JSONResponse(status_code=401, content={"error": str(exc)})
        return inner
    return decorator
