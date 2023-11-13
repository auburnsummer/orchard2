from typing import Never
from httpx import AsyncClient
from orchard.libs.discord_msgspec.user import DiscordUser
from orchard.projects.v1.models.credentials import DiscordCredential
from orchard.projects.v1.models.engine import insert, select
from orchard.projects.v1.models.users import User
import pytest
from unittest.mock import patch

from orchard.projects.v1.routes.discord_auth import DiscordAuthCallbackHandlerArgs
from orchard.projects.v1.core.auth import paseto_to_token


@pytest.fixture
def mock_get_discord_user_from_oauth():
    async def mock(data: DiscordAuthCallbackHandlerArgs):
        if data.code == "mockcode":
            return DiscordUser(id="testid", username="mafuyu", avatar="testavatar", global_name="yuki")
        if data.code == "mockcode2":
            return DiscordUser(id="testid", username="mafuyu", avatar=None, global_name="yuki")

    with patch("orchard.projects.v1.routes.discord_auth.get_discord_user_from_oauth", new=mock):
        yield

@pytest.mark.asyncio
async def test_discord_auth_creates_new_user_if_no_credential_exists(
    mock_get_discord_user_from_oauth: Never,
    client: AsyncClient
):
    # prior to calling the endpoint, there is no user called mafuyu.
    all_users = list(select(User).all())
    assert all_users == []

    resp = await client.post("/auth/token/discord", json={
        "code": "mockcode",
        "redirect_uri": "http://testserver"
    })
    assert resp.status_code == 200

    all_users = list(select(User).all())

    assert len(all_users) == 1
    assert all_users[0].name == "yuki"

    # and there should also be a credential created.
    cred = select(DiscordCredential).by_id("testid")
    assert cred is not None
    assert cred.id == "testid"
    assert cred.user == all_users[0]

    # # and the token returned should be valid.
    token = resp.json()["token"]
    assert paseto_to_token(token).User_all == all_users[0].id

@pytest.mark.asyncio
async def test_discord_auth_returns_existing_user(
    mock_get_discord_user_from_oauth: Never, 
    client: AsyncClient
):
    user = User.new(name="mafuyu")
    cred = DiscordCredential(
        id="testid",
        user=user
    )
    insert(cred)
    users = list(select(User).all())
    assert users == [user]

    resp = await client.post("/auth/token/discord", json={
        "code": "mockcode",
        "redirect_uri": "http://testserver"
    })
    assert resp.status_code == 200

    users = list(select(User).all())
    assert len(users) == 1

    # and the token returned should be valid.
    token = resp.json()["token"]
    assert paseto_to_token(token).User_all == users[0].id

@pytest.mark.asyncio
async def test_discord_auth_updates_details(
    mock_get_discord_user_from_oauth: Never,
    client: AsyncClient
):
    user = User.new(name="mafuyu")
    cred = DiscordCredential(
        id="testid",
        user=user
    )
    insert(cred)
    users = list(select(User).all())
    assert users == [user]

    resp = await client.post("/auth/token/discord", json={
        "code": "mockcode",
        "redirect_uri": "http://testserver"
    })
    assert resp.status_code == 200

    user = select(User).by_id(user.id)
    assert user.name == "yuki"
    assert user.avatar_url == "https://cdn.discordapp.com/avatars/testid/testavatar"

@pytest.mark.skip
@pytest.mark.asyncio
async def test_discord_auth_does_not_update_avatar_url_if_they_dont_have_one(
    mock_get_discord_user_from_oauth: Never,
    client: AsyncClient
):
    user = User.new(name="mafuyu")
    user.avatar_url = "fjiewjfoiwejfweof"
    cred = DiscordCredential(
        id="testid",
        user=user
    )
    insert(cred)
    users = list(select(User).all())
    assert users == [user]

    resp = await client.post("/auth/token/discord", json={
        "code": "mockcode2",
        "redirect_uri": "http://testserver"
    })
    assert resp.status_code == 200

    user = select(User).by_id(user.id)
    assert user.name == "yuki"
    assert user.avatar_url is None

