from .base import BaseDiscordStruct

class OAuthTokenResponse(BaseDiscordStruct):
    """
    https://discord.com/developers/docs/topics/oauth2#authorization-code-grant-access-token-response
    """
    access_token: str
    expires_in: int
    refresh_token: str
    scope: str
    token_type: str
