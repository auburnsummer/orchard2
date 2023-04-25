"""AUTH

General goals.

Users can "log in With Discord". This means they have possession of a token which
proves their identity. 

In general, our endpoints will simply use Discord tokens as auth. So we don't have
our own tokens at all. Just Discord tokens.

The client knows what the Discord token is, and therefore can make calls to the
Discord API on their own. This isn't _too_ useful, because we only request a token
with pretty minimal permissions (identify, guilds.members.read) 

General flow is kinda like this:

 1. user clicks on a "Log in To Discord" link in client. This links to

  https://discord.com/api/oauth2/authorize?client_id=1096424315718733927&redirect_uri=https%3A%2F%2Fexample.com&response_type=code&scope=identify,guild.members.read

  e.g. except the redirect_uri will be back to us.

 2. after login, user is now at 

  rhythm.cafe/login_callback?code=blahblahblah

 3. Remix (in the "server side" on the /login_callback handler) takes the query param code and calls our API with it to get an actual discord token.

  POST api.rhythm.cafe/api/token
    {
        "code": "....."
    }

 4. On the Python end, when we get this, we:

  1. Generate a token and refresh token by calling discord API
  2. Return the token and the refresh. 

 5. Remix then calls a different api, /users/create, with the info to populate the initial object.

 6. The Remix handler then returns `/` route with a cookie set of the token. It can use this token to get stuff

"""

from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
import httpx
from pydantic import BaseModel
from v1.dependencies.client_nonrestricted import client_nonrestricted
from v1.env import ENV
from v1.models.discord import OAuthErrorResponse, OAuthTokenResponse


auth_routes = APIRouter()

@auth_routes.get("/client_id")
def get_client_id():
    """
    Get the Discord client_id of the app. This is used to get the correct authentication url
    """
    return ENV.discord_client_id


class GetTokenPayload(BaseModel):
    code: str
    redirect_uri: str


@auth_routes.post(
    "/token",
    responses={
        200: {"model": OAuthTokenResponse},
        400: {"model": OAuthErrorResponse}
    }
)
async def get_token(payload: GetTokenPayload, client: Annotated[httpx.AsyncClient, Depends(client_nonrestricted)]) -> OAuthTokenResponse | OAuthErrorResponse:
    """
    Convert a OAuth code into a Discord token.

    Note: The app uses Discord tokens as authentication for endpoints.
    """
    resp = await client.post("https://discord.com/api/oauth2/token", data={
        "grant_type": "authorization_code",
        "client_id": ENV.discord_client_id,
        "client_secret": ENV.discord_client_secret.get_secret_value(),
        "code": payload.code,
        "redirect_uri": payload.redirect_uri
    })
    parsed = resp.json()
    if resp.is_success:
        token = OAuthTokenResponse(**parsed)
        return token
    else:
        return JSONResponse(status_code=400, content=OAuthErrorResponse(**parsed).dict())