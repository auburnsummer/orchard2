import httpx

from oauthlogin.providers import OAuthProvider, OAuthToken, OAuthUser


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
        )

    def get_oauth_user(self, *, oauth_token):
        response = httpx.get(
            "https://discord.com/api/users/@me",
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {oauth_token.access_token}",
            },
        )
        response.raise_for_status()
        data = response.json()
        return OAuthUser(
            id=data["id"],
            username=data["username"],
            email=data["email"],
        )