from typing import Annotated, TypeAlias
from fastapi import Depends, HTTPException, Header, status
from pydantic import ValidationError
import pyseto
import json

from v1.dependencies.client_nonrestricted import ClientNonrestricted
from v1.dependencies.session import InjectedSession
from v1.dependencies.tokens import PasetoKey
from v1.models.discord import DiscordErrorResponse, DiscordUser
from v1.models.sessions import OrchardSessionToken
from v1.models.user import User, UserCombined

from v1.env import ENV

from sqlmodel import select


async def injected_token(authorization: Annotated[str, Header()], key: PasetoKey):
    """
    Dependency that gets the token from the Bearer header and decodes it.
    """
    payload = authorization.replace("Bearer ", "")
    token = pyseto.decode(key, payload)
    parsed = json.loads(token.payload.decode("utf-8"))
    return OrchardSessionToken(**parsed)


InjectedToken: TypeAlias = Annotated[OrchardSessionToken, Depends(injected_token)]

async def injected_orchard_user(token: InjectedToken, session: InjectedSession):
    """
    Dependency that injects the current user from the token.
    """
    print(token)
    # get the user from the database. the id is the sub of the token.
    select_statement = select(User).where(User.discord_id == token.sub)
    result = session.exec(select_statement).first()
    if result:
        logout_time = result.logout_time
        if token.iat < logout_time:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token has been revoked.")
        return result
    else:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "User does not exist.")


InjectedUser: TypeAlias = Annotated[User, Depends(injected_orchard_user)]

async def injected_discord_user(user: InjectedUser, client: ClientNonrestricted):
    """
    Dependency that injects the Discord user info, given a user.

    This requires a Discord API call, so only use this if you need the Discord user info.
    """
    user_id = user.discord_id
    resp = await client.get(f"https://discord.com/api/v10/users/{user_id}", headers={
        "Authorization": f"Bot {ENV.discord_bot_api_key.get_secret_value()}"
    })
    payload = resp.json()
    if resp.is_success:
        try:
            parsed = DiscordUser(**payload)
            return parsed
        except ValidationError as e:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, e.json())
    else: 
        parsed = DiscordErrorResponse(**payload)
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, parsed.dict())


InjectedDiscordUser: TypeAlias = Annotated[DiscordUser, Depends(injected_discord_user)]


async def injected_user(discord_user: InjectedDiscordUser, orchard_user: InjectedUser):
    """
    A combined dict of both the InjectedDiscordUser and InjectedOrchardUser.

    Has the same API call considerations as InjectedDiscordUser.
    """
    return UserCombined(**discord_user.dict(), **orchard_user.dict())


InjectedUserFull: TypeAlias = Annotated[UserCombined, Depends(injected_user)]