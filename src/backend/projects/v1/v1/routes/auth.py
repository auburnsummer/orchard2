"""AUTH

General goals.

Users can "log in With Discord". This means they have possession of a token which
proves their identity. 

In general, our endpoints will simply use Discord tokens as auth. So we don't have
our own tokens at all. Just Discord tokens.

The client knows what the Discord token is, and therefore can make calls to the
Discord API on their own. This isn't _too_ useful, because we only request a token
with pretty minimal permissions (identify, guilds.members.read) 

Some API endpoints require further checks. such as 

 1. user clicks on a "Log in To Discord" link in client. This links to

  https://discord.com/api/oauth2/authorize?client_id=1096424315718733927&redirect_uri=https%3A%2F%2Fexample.com&response_type=code&scope=identify,guild.members.read

  e.g. except the redirect_uri will be back to us.

 2. after login, user is now at 

  rhythm.cafe/login_callback?code=blahblahblah

 3. Remix (in the "server side" on the /login_callback handler) takes the code and calls our API with it to get an actual discord token. this is what's passed into our API _and_ discord's api.

  POST api.rhythm.cafe/api/token
    {
        "code": "....."
    }

 4. On the Python end, when we get this, we do a few things:

  1. Generate a token and refresh token by calling discord API
  2. Populate the User table with the info, expiry date, refresh token.
     - The refresh token should be encrypted at rest.
     - Existing expiry date / refresh token is replaced if exists.
     - Expiry date is a datetime.
  3. Return the token (but not the refresh).

 5. The Remix handler then returns `/` route with a cookie set of the token. It can use this token to get stuff

"""

from fastapi import APIRouter
from v1.env import ENV

auth_routes = APIRouter()

@auth_routes.get("/client_id")
def get_client_id():
    return ENV.discord_client_id