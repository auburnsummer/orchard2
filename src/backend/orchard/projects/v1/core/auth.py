"""
Auth tokens are PASETO tokens encoding the user.
"""

from base64 import b64decode
import json

from pydantic import BaseModel, Field
from .config import config

import pyseto

from datetime import datetime
from functools import wraps
from typing import Callable, Optional, Set

from starlette.requests import Request
from starlette.responses import JSONResponse

class OrchardAuthToken(BaseModel):
    iat: datetime
    exp: datetime
    # tokens have claims attached to them.
    # claim: the token belongs to this user.
    user: Optional[str] = Field(default=None)

paseto_key = pyseto.Key.new(version=4, purpose="local", key=b64decode(config().PASETO_KEY_BASE64.get_secret_value()))

"""
Token generation:
from orchard.projects.v1.core.auth import OrchardAuthToken, token_to_paseto
from datetime import datetime, timedelta

token = OrchardAuthToken(iat=datetime.now(), exp=datetime.now() + timedelta(hours=1)) # other args as reqd
paseto = token_to_paseto(token)
"""

def _token_to_paseto(token: OrchardAuthToken):
    payload = token.model_dump(mode="json")
    exp_time_in_seconds = int((token.exp - token.iat).total_seconds())
    encoded_token = pyseto.encode(
        key=paseto_key,
        payload=payload,
        serializer=json,
        exp=exp_time_in_seconds
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
    print(token.payload)
    return OrchardAuthToken(**token.payload)


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
                parsed_dict = parsed_token.model_dump()
                for scope in scopes:
                    if parsed_dict[scope] is None:
                        raise InvalidToken(f"Token lacks the required scope: {scope}")
                else:
                    request.state.token = parsed_token
                    return await func(request)
            except InvalidToken as exc:
                return JSONResponse(status_code=401, content={"error": str(exc)})
        return inner
    return decorator
