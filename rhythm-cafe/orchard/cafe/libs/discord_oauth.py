from django.http import HttpRequest
from django.urls import reverse
import httpx
from django.utils import timezone
import datetime
from oauthlogin.providers import OAuthProvider, OAuthToken, OAuthUser
from .errors import OrchardException

from functools import cache

class DiscordUserNotVerified(OrchardException):
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
        return OAuthToken(
            access_token=data["access_token"],
            refresh_token=data["refresh_token"],
            access_token_expires_at=timezone.now() + datetime.timedelta(seconds=data["expires_in"])
        )

    def get_oauth_user(self, *, oauth_token):
        data = get_discord_user_from_oauth(oauth_token.access_token)

        # from testing, Discord seems to block the oauth on their end if the user is not verified.
        # but we'll check ourselves to be safe.
        if not data['verified']:
           raise DiscordUserNotVerified("User needs to have a verified email")
        
        display_name = data["global_name"] if "global_name" in data.keys() else data["username"]

        return OAuthUser(
            id=data["id"],
            username=display_name,  # doesn't need to be unique
            email=data["email"],
        )
    
    def refresh_oauth_token(self, *, oauth_token: OAuthToken) -> OAuthToken:
        response = httpx.post(
            "https://discord.com/api/oauth2/token",
            headers={
                "Accept": "application/json"
            },
            data={
                "grant_type": "refresh_token",
                "client_id": self.get_client_id(),
                "client_secret": self.get_client_secret(),
                "refresh_token": oauth_token.refresh_token
            }
        )
        response.raise_for_status()
        data = response.json()
        return OAuthToken(
            access_token=data["access_token"],
            refresh_token=data["refresh_token"],
            access_token_expires_at=timezone.now() + datetime.timedelta(seconds=data["expires_in"])
        )