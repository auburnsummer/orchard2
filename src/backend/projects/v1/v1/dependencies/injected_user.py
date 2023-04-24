from typing import Annotated, TypeAlias
from fastapi import Depends, HTTPException, JSONResponse, Header, status
import httpx
from pydantic import BaseModel, ValidationError

from v1.dependencies.client_nonrestricted import ClientNonrestricted
from v1.models.discord import ErrorResponse, DiscordUser


async def injected_user(bearer: Annotated[str, Header()], client: ClientNonrestricted):
    """
    Dependency that injects the current user from the Bearer header. The Bearer token is directly a Discord token,
    so we have to make an API call to find out who the user is.

    The ratelimit on this call is really generous, so for now I'm using ClientNonrestricted for it.

    TODO: memoize the Discord API call if required.
    """
    resp = await client.get("https://discord.com/api/v10/users/@me", headers={
        "Authorization": bearer
    })
    if resp.is_success:
        try:
            parsed = DiscordUser(**resp.json())
            return parsed
        except ValidationError as e:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, e.json())
    else:
        parsed = ErrorResponse(**parsed)
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, ErrorResponse(**parsed).dict())


InjectedUser: TypeAlias = Annotated[DiscordUser, Depends(injected_user)]