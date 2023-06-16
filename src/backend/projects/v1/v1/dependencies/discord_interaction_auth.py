"""
Discord interactions send authentication data in the request headers.

Details here: https://discord.com/developers/docs/interactions/receiving-and-responding#security-and-authorization
"""

from typing import Annotated, TypeAlias, Never
from fastapi import HTTPException, Header, Request, status, Depends
from v1.libs.env import env
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.exceptions import InvalidSignature


async def discord_interaction_auth(X_Signature_Ed25519: Annotated[str, Header()], X_Signature_Timestamp: Annotated[str, Header()], request: Request):
    """
    Dependency that validates the Discord interaction request headers.

    This is a dependency that you can use in your FastAPI route to validate the Discord interaction request headers.
    """
    public_key = env().discord_bot_public_key
    verify_key = Ed25519PublicKey.from_public_bytes(bytes.fromhex(public_key))
    payload = await request.body()
    # concat bytes together
    to_verify = X_Signature_Timestamp.encode("ascii") + payload

    try:
        verify_key.verify(bytes.fromhex(X_Signature_Ed25519), to_verify)
        yield
    except InvalidSignature:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid request signature")


RequiresDiscordAuth: TypeAlias = Annotated[Never, Depends(discord_interaction_auth)]