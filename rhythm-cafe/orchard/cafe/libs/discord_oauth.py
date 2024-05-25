import httpx
from django.utils import timezone
import datetime
from oauthlogin.providers import OAuthProvider, OAuthToken, OAuthUser

from functools import cache

class DiscordUserNotVerified(Exception):
    pass

@cache
def get_discord_user_from_oauth(bearer_token: str):
    response = httpx.get(
        "https://discord.com/api/users/@me",
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {bearer_token}",
        },
    )
    data = response.json()
    response.raise_for_status()
    return data

class DiscordOAuthProvider(OAuthProvider):
    authorization_url = "https://discord.com/oauth2/authorize"

    def get_oauth_token(self, *, code, request):
        response = httpx.post(
            "https://discord.com/api/oauth2/token",
            headers={
                "Accept": "application/json",
            },
            data={
                "grant_type": "authorization_code",
                "client_id": self.get_client_id(),
                "client_secret": self.get_client_secret(),
                "code": code,
                "redirect_uri": self.get_callback_url(request=request)
            },
        )
        response.raise_for_status()
        data = response.json()
        print(data)
        return OAuthToken(
            access_token=data["access_token"],
            refresh_token=data["refresh_token"],
            access_token_expires_at=timezone.now() + datetime.timedelta(seconds=data["expires_in"])
        )

    def get_oauth_user(self, *, oauth_token):
        data = get_discord_user_from_oauth(oauth_token.access_token)

        #if True:
        #    raise DiscordUserNotVerified("User needs to have a verified email")
        
        display_name = data["global_name"] if "global_name" in data.keys() else data["username"]

        return OAuthUser(
            id=data["id"],
            username=display_name,  # doesn't need to be unique
            # TODO: check what happens if email is not verified
            email=data["email"],
        )