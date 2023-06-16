from base64 import b64decode
from typing import Annotated, TypeAlias, Tuple
from v1.libs.env import env
from fastapi import Depends

from pyseto import Key, KeyInterface, encode
from v1.models.sessions import OrchardSessionToken

from datetime import datetime, timedelta

import json

def get_paseto_key():
    key_bytes = b64decode(env().paseto_key_base64.get_secret_value())
    key = Key.new(version=4, purpose='local', key=key_bytes) 
    return key

PasetoKey: TypeAlias = Annotated[KeyInterface, Depends(get_paseto_key)]

def session_token_to_key(token: OrchardSessionToken, key: PasetoKey) -> str:
    encoded_session_token = token.json().encode('utf-8')
    token = encode(key, encoded_session_token, serializer=json)
    return token.decode("utf-8")

def make_user_session_token(user_id: str, key: PasetoKey) -> Tuple[str, timedelta]:
    expiry = timedelta(days=14)
    token = OrchardSessionToken(sub=user_id, iat=datetime.now(), exp=datetime.now() + expiry) # 14 days
    return session_token_to_key(token, key), expiry