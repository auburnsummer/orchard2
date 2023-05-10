"""AUTH

General goals.

Users can "log in With Discord". This means they have possession of a token which
proves their identity. 

Our tokens are pasetos signed by us. They contain the user's discord id and when the token
was issued.

Tokens _do not_ contain the original discord token. I only care about the user id, if I
want to get info about the user I can use the /user/{id} endpoint instead of the /me endpoint;

which will work as long as the user is in a guild with the bot. which they _should be_ if they're
using the app.

General flow is kinda like this:

 1. user clicks on a "Log in To Discord" link in client. This links to

  https://discord.com/api/oauth2/authorize?client_id=1096424315718733927&redirect_uri=https%3A%2F%2Fexample.com&response_type=code&scope=identify,guild.members.read

  e.g. except the redirect_uri will be back to us.

 2. after login, user is now at 

  rhythm.cafe/login_callback?code=blahblahblah 

 3. Remix (in the "server side" on the /login_callback handler) takes the query param code and calls our API with it...

  POST api.rhythm.cafe/api/token
    {
        "code": "....."
    }

 4. On the Python end, when we get this, we:

  1. Generate a token and refresh token by calling discord API
  2. Use the token to call the /users/@me endpoint to get the user's info
  3. Generate a paseto encoding the user's id and the token issue date
  4. Revoke the discord token? (maybe not, maybe we can just let it expire)
  5. Return the paseto to the client.
  6. (we threw away the refresh token, we don't need it)

 5. Remix then calls a different api, /users/create, with the info to populate the initial object.

 6. The Remix handler then returns `/` route with a cookie set of the paseto.

"""

import json
from typing import Annotated
from fastapi import APIRouter, Depends, Header, HTTPException, status
from fastapi.responses import JSONResponse
import httpx
from pydantic import BaseModel
import pyseto
from v1.dependencies.client_nonrestricted import ClientNonrestricted
from v1.dependencies.injected_user import InjectedDiscordUser, InjectedUser
from v1.dependencies.session import InjectedSession
from v1.dependencies.tokens import PasetoKey, session_token_to_key
from v1.env import env
from v1.models.discord import OAuthErrorResponse, OAuthTokenResponse, DiscordUser
from v1.models.sessions import OrchardSessionToken, OrchardTokenResponse

from datetime import datetime, timedelta
from json import dumps 

auth_routes = APIRouter()

@auth_routes.get("/client_id")
def get_client_id():
    """
    Get the Discord client_id of the app. This is used to get the correct authentication url
    """
    return env().discord_client_id


class PostTokenPayload(BaseModel):
    code: str
    redirect_uri: str


@auth_routes.post(
    "/token",
    response_model=OrchardTokenResponse
)
async def get_token(
    payload: PostTokenPayload,
    client: ClientNonrestricted,
    key: PasetoKey
) -> OAuthTokenResponse | OAuthErrorResponse:
    """
    Convert a OAuth code into a paseto authenticating the user.
    """
    # turn the code into a token.
    resp = await client.post("https://discord.com/api/oauth2/token", data={
        "grant_type": "authorization_code",
        "client_id": env().discord_client_id,
        "client_secret": env().discord_client_secret.get_secret_value(),
        "code": payload.code,
        "redirect_uri": payload.redirect_uri
    })
    parsed = resp.json()
    if resp.is_success:
        token_response = OAuthTokenResponse(**parsed)
        # we have a token, but we don't know the id yet. 
        user_resp = await client.get("https://discord.com/api/users/@me", headers={
            "Authorization": f"Bearer {token_response.access_token}"
        })
        user_parsed = user_resp.json()
        if user_resp.is_success:
            user = DiscordUser(**user_parsed)
            user_id = user.id
            # create a paseto token encapsulating the id, but not the original token. 
            # the original token has never been sent to the client, so we don't need to revoke it.
            expiry = timedelta(days=14)
            session_token = OrchardSessionToken(sub=user_id, iat=datetime.now(), exp=datetime.now() + expiry) # 14 days
            token = session_token_to_key(session_token, key)
            return OrchardTokenResponse(token=token, expires_in=int(expiry.total_seconds()))
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Could not find user")
    else:
        raise HTTPException(status_code=400, detail=OAuthErrorResponse(**parsed).dict())



@auth_routes.post(
    "/revoke"
)
async def revoke_token(user: InjectedUser, session: InjectedSession):
    # how do we revoke a paseto?
    # each user has a "global signout date", which is a datetime stored in the db.
    # whenever a token is used, check if the paseto was issued before the global signout. if it was, reject it.
    # then, revoking a token is just a matter of setting the global signout date to now.
    # ...of course, this means we can't revoke individual tokens, but that's fine.
    user.logout_time = datetime.now()
    session.add(user)
    session.commit()

    return {"success": True}
