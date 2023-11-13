"""
Routes relating to discord oauth login.
"""

from datetime import timedelta
from orchard.libs.discord_msgspec.oauth import OAuthTokenResponse
from orchard.libs.discord_msgspec.user import DiscordUser
from orchard.projects.v1.core.auth import OrchardAuthScopes, make_token_now
from orchard.projects.v1.core.forward import forward_httpx
from orchard.projects.v1.core.wrapper import msgspec_return, parse_body_as

from httpx import AsyncClient, HTTPStatusError

from orchard.projects.v1.core.config import config
from orchard.projects.v1.models.credentials import DiscordCredential
from orchard.projects.v1.models.engine import select, insert, update
from orchard.projects.v1.models.users import User
from starlette.requests import Request

import msgspec

class DiscordAuthCallbackHandlerArgs(msgspec.Struct):
    code: str
    redirect_uri: str

async def get_discord_user_from_oauth(data: DiscordAuthCallbackHandlerArgs):
    fig = config()
    async with AsyncClient() as client:
        resp = await client.post("https://discord.com/api/oauth2/token", data={
            "grant_type": "authorization_code",
            "client_id": fig.DISCORD_APPLICATION_ID,
            "client_secret": fig.DISCORD_CLIENT_SECRET.get_secret_value(),
            "code": data.code,
            "redirect_uri": data.redirect_uri
        })
        resp.raise_for_status()
        token_response = msgspec.json.decode(resp.content, type=OAuthTokenResponse)
        # we have a token, but we don't know the id yet. 
        user_resp = await client.get("https://discord.com/api/users/@me", headers={
            "Authorization": f"Bearer {token_response.access_token}"
        })
        discord_user = msgspec.json.decode(user_resp.content, type=DiscordUser)
    return discord_user


# https://discord.com/api/oauth2/authorize?client_id=1096424315718733927&redirect_uri=https%3A%2F%2Fexample.com&response_type=code&scope=identify

class DiscordTokenResponse(msgspec.Struct):
    token: str
    expires_in: int

@msgspec_return(status_code=200)
@parse_body_as(DiscordAuthCallbackHandlerArgs)
async def discord_token_handler(request: Request):
    "Log in with discord. Gets a discord token and returns our token."
    data: DiscordAuthCallbackHandlerArgs = request.state.body

    try:
        discord_user = await get_discord_user_from_oauth(data)
    except HTTPStatusError as e:
        return forward_httpx(e.response)
    
    cred = select(DiscordCredential).by_id(discord_user.id)
    if not cred:
        # make a new user.
        user = User.new(name=discord_user.global_name)
        cred = DiscordCredential(id=discord_user.id, user=user)
        insert(cred) # the user is inserted also.

    should_update = False

    user = cred.user
    # if the name is different, update the stored name.
    if user.name != discord_user.global_name:
        should_update = True
        user.name = discord_user.global_name

    # if the avatar is different, update the avatar.
    if discord_user.avatar:
        avatar_url = f"https://cdn.discordapp.com/avatars/{discord_user.id}/{discord_user.avatar}"
        if user.avatar_url != avatar_url:
            user.avatar_url = avatar_url
            should_update = True

    if should_update:
        update(user)

    # create a scoped token for this user.
    # the original token has never been sent to the client, so we don't need to revoke it.
    exp_time = timedelta(days=7)
    orch_token = make_token_now(OrchardAuthScopes(User_all=user.id), exp_time)
    return DiscordTokenResponse(token=orch_token, expires_in=exp_time.total_seconds())