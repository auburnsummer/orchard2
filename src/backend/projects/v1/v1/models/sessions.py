"""
Sessions are paseto tokens. They are signed by us, and contain the user's discord id and when the token was issued.
We don't store them anywhere, because they're signed by us so we can verify them.

Session tokens cannot be revoked. Instead, the user can log out, which will set the logout_time field on their user,
and we treat any tokens issued before that time as invalid.
"""

from pydantic import BaseModel
from datetime import datetime


class OrchardSessionToken(BaseModel):
    sub: str  # discord id
    iat: datetime
    exp: int


class OrchardTokenResponse(BaseModel):
    token: str
    expires_in: int