from typing import Annotated, TypeAlias
from fastapi import Depends, HTTPException, Header, status
from pydantic import ValidationError

from v1.dependencies.client_nonrestricted import ClientNonrestricted
from v1.dependencies.session import InjectedSession
from v1.models.discord import DiscordErrorResponse, DiscordUser
from v1.models.user import User, UserCombined

from sqlmodel import select

async def injected_user(authorization: Annotated[str, Header()], client: ClientNonrestricted):
    """
    Dependency that injects the current Discord user from the Bearer header. The Bearer token is directly a Discord token,
    so we have to make an API call to find out who the user is.
 
    The ratelimit on this call is really generous, so for now I'm using ClientNonrestricted for it.

    TODO: memoize the Discord API call if required.
    """
    resp = await client.get("https://discord.com/api/v10/users/@me", headers={
        "Authorization": authorization
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



InjectedDiscordUser: TypeAlias = Annotated[DiscordUser, Depends(injected_user)]


async def injected_orchard_user(user: InjectedDiscordUser, session: InjectedSession):
    """
    Dependency that injects the orchard user from the db. The user must exist.
    """
    user_id = user.id
    select_statement = select(User).where(User.discord_id == user_id)
    existing_user = session.exec(select_statement).first()
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist.")
    return existing_user


InjectedOrchardUser: TypeAlias = Annotated[User, Depends(injected_orchard_user)]


async def injected_user(discord_user: InjectedDiscordUser, orchard_user: InjectedOrchardUser):
    """
    A combined dict of both the InjectedDiscordUser and InjectedOrchardUser.

    Typically, just use this! :D
    """
    return UserCombined(**discord_user.dict(), **orchard_user.dict())


InjectedUser: TypeAlias = Annotated[UserCombined, Depends(injected_user)]