from fastapi.testclient import TestClient
import httpx
from sqlmodel import Session
from v1.dependencies.tokens import get_paseto_key, session_token_to_key
from v1.dependencies.injected_user import injected_token
from v1.models.discord import DiscordUser, OAuthTokenResponse
from v1.models.sessions import OrchardTokenResponse, OrchardSessionToken
from v1.models.user import User

from datetime import datetime, timedelta

def test_get_auth_client_id_returns_the_client_id(client: TestClient):
    resp = client.get("/auth/client_id")
    assert resp.status_code == 200
    assert resp.json() == "MOCK_discord_client_id"


def test_post_auth_token_returns_a_token(client: TestClient, httpx_mock):
    mock_token = OAuthTokenResponse(access_token='MOCK_access_token', token_type='MOCK_token_type', expires_in=123, refresh_token='MOCK_refresh_token', scope='MOCK_scope')
    httpx_mock.add_response(url="https://discord.com/api/oauth2/token", text=mock_token.json())

    mock_discord_user = DiscordUser(id="MOCK_id", username="MOCK_username", discriminator="MOCK_discriminator", avatar="MOCK_avatar")
    httpx_mock.add_response(url="https://discord.com/api/users/@me", text=mock_discord_user.json())

    resp = client.post("/auth/token", json={
        "code": "MOCK_code",
        "redirect_uri": "MOCK_redirect_uri"
    })
    assert resp.status_code == 200
    result = OrchardTokenResponse(**resp.json())
    assert result.expires_in == 1209600

    key = get_paseto_key()
    user = injected_token(f"Bearer {result.token}", key)
    assert user.sub == "MOCK_id"
    assert user.exp > datetime.now()


def test_post_revoke_sets_logout_time(client: TestClient, session: Session, user1: User, user1_token: str):
    resp = client.post("/auth/revoke", headers={
        "Authorization": f"Bearer {user1_token}"
    })
    assert resp.status_code == 200

    session.refresh(user1)
    assert user1.logout_time > datetime.fromtimestamp(0)
