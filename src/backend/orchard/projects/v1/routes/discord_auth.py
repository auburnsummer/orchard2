"""
Routes relating to discord oauth login.
"""

from datetime import timedelta
from orchard.projects.v1.core.auth import OrchardAuthScopes, OrchardAuthToken, make_token_now
from pydantic import BaseModel

from httpx import AsyncClient

from orchard.projects.v1.core.config import config
from orchard.projects.v1.models.credentials import create_or_get_user_with_credential
from orchard.projects.v1.models.users import update_user, EditUser
from starlette.responses import JSONResponse

class OAuthTokenResponse(BaseModel):
    access_token: str
    expires_in: int
    refresh_token: str
    scope: str
    token_type: str

class DiscordAuthCallbackHandlerArgs(BaseModel):
    code: str
    redirect_uri: str

class DiscordUserPartial(BaseModel):
    id: str
    username: str


async def get_discord_user_from_oauth(data: DiscordAuthCallbackHandlerArgs):
    C = config()
    async with AsyncClient() as client:
        resp = await client.post("https://discord.com/api/oauth2/token", data={
            "grant_type": "authorization_code",
            "client_id": C.DISCORD_APPLICATION_ID,
            "client_secret": C.DISCORD_CLIENT_SECRET.get_secret_value(),
            "code": data.code,
            "redirect_uri": data.redirect_uri
        })
        token_response = OAuthTokenResponse(**resp.json())
        # we have a token, but we don't know the id yet. 
        user_resp = await client.get("https://discord.com/api/users/@me", headers={
            "Authorization": f"Bearer {token_response.access_token}"
        })
        discord_user = DiscordUserPartial(**user_resp.json())
    return discord_user


# https://discord.com/api/oauth2/authorize?client_id=1096424315718733927&redirect_uri=https%3A%2F%2Fexample.com&response_type=code&scope=identify

async def discord_token_handler(request):
    data = DiscordAuthCallbackHandlerArgs(**await request.json())

    discord_user = await get_discord_user_from_oauth(data)
    
    user, _ = await create_or_get_user_with_credential(discord_user.id, discord_user.username)
    # if the name is different, update the stored name.
    if user.name != discord_user.username:
        await update_user(user.id, EditUser(name=discord_user.username))

    # create a scoped token for this user.
    # the original token has never been sent to the client, so we don't need to revoke it.
    exp_time = timedelta(days=7)
    orch_token = make_token_now(OrchardAuthScopes(user=user.id), exp_time)
    return JSONResponse({
        "token": orch_token,
        "expires_in": exp_time.total_seconds()
    }, status_code=200)