from typing import Never
from httpx import AsyncClient
import pytest
from unittest.mock import patch

from orchard.projects.v1.routes.discord_auth import DiscordAuthCallbackHandlerArgs, DiscordUserPartial
from orchard.projects.v1.models.users import get_all_users
from orchard.projects.v1.models.credentials import get_disc_credential, make_new_user_with_credential
from orchard.projects.v1.core.auth import paseto_to_token

@pytest.fixture
def mock_get_discord_user_from_oauth():
    async def mock(data: DiscordAuthCallbackHandlerArgs):
        if data.code == "mockcode":
            return DiscordUserPartial(id="testid", username="mafuyu", avatar="testavatar")
        if data.code == "mockcode2":
            return DiscordUserPartial(id="testid", username="mafuyu", avatar=None)

    with patch("orchard.projects.v1.routes.discord_auth.get_discord_user_from_oauth", new=mock):
        yield


@pytest.mark.asyncio
async def test_discord_auth_creates_new_user_if_no_credential_exists(
    mock_get_discord_user_from_oauth: Never, 
    client: AsyncClient
):
    # prior to calling the endpoint, there is no user called mafuyu.
    assert (await get_all_users()) == []

    resp = await client.post("/auth/token/discord", json={
        "code": "mockcode",
        "redirect_uri": "http://testserver"
    })
    assert resp.status_code == 200

    users = await get_all_users()
    assert len(users) == 1
    assert users[0].name == "mafuyu"

    # and there should also be a credential created.
    cred = await get_disc_credential("testid")
    assert cred.id == "testid"
    assert cred.user_id == users[0].id

    # and the token returned should be valid.
    token = resp.json()["token"]
    assert paseto_to_token(token).user == users[0].id

@pytest.mark.asyncio
async def test_discord_auth_returns_existing_user(
    mock_get_discord_user_from_oauth: Never, 
    client: AsyncClient
):
    user, cred = await make_new_user_with_credential("testid", "mafuyu")
    users = await get_all_users()
    assert users == [user]

    resp = await client.post("/auth/token/discord", json={
        "code": "mockcode",
        "redirect_uri": "http://testserver"
    })
    assert resp.status_code == 200

    users = await get_all_users()
    assert len(users) == 1

    # and the token returned should be valid.
    token = resp.json()["token"]
    assert paseto_to_token(token).user == users[0].id

@pytest.mark.asyncio
async def test_discord_auth_updates_name_if_discord_name_is_different(
    mock_get_discord_user_from_oauth: Never,
    client: AsyncClient
):
    users = await get_all_users()
    assert users == []

    user, cred = await make_new_user_with_credential("testid", "yuki")
    users = await get_all_users()
    assert users == [user]
    assert users[0].name == "yuki"

    resp = await client.post("/auth/token/discord", json={
        "code": "mockcode",
        "redirect_uri": "http://testserver"
    })
    print(resp.json())
    resp.raise_for_status()
    assert resp.status_code == 200

    # the credential will have name mafuyu.
    users = await get_all_users()
    assert len(users) == 1
    assert users[0].name == "mafuyu"


@pytest.mark.asyncio
async def test_discord_auth_updates_avatar_url_if_they_have_one(
    mock_get_discord_user_from_oauth: Never,
    client: AsyncClient
):
    user, cred = await make_new_user_with_credential("testid", "mafuyu")
    users = await get_all_users()
    assert users == [user]

    resp = await client.post("/auth/token/discord", json={
        "code": "mockcode",
        "redirect_uri": "http://testserver"
    })
    assert resp.status_code == 200

    users = await get_all_users()
    assert users[0].avatar_url == "https://cdn.discordapp.com/avatars/testid/testavatar"


@pytest.mark.asyncio
async def test_discord_auth_does_not_update_avatar_url_if_they_dont_have_one(
    mock_get_discord_user_from_oauth: Never,
    client: AsyncClient
):
    user, cred = await make_new_user_with_credential("testid", "mafuyu")
    users = await get_all_users()
    assert users == [user]

    resp = await client.post("/auth/token/discord", json={
        "code": "mockcode2",
        "redirect_uri": "http://testserver"
    })
    assert resp.status_code == 200

    users = await get_all_users()
    assert users[0].avatar_url is None
