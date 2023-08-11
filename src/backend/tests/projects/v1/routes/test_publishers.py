from httpx import AsyncClient
from orchard.projects.v1.core.auth import OrchardAuthScopes, make_token_now
from orchard.projects.v1.models.discord_guild_credentials import get_disc_guild_credential
from orchard.projects.v1.models.publishers import get_all_publishers
from orchard.projects.v1.models.metadata import engine
import pytest
from datetime import timedelta

@pytest.fixture
def discord_guild_token_1():
    return make_token_now(
        scopes=OrchardAuthScopes(
            discord_guild="discord_guild_id"
        ),
        exp_time=timedelta(days=1)
    )

@pytest.mark.asyncio
async def test_publisher_new_creates_a_new_publisher_and_credential(client: AsyncClient, discord_guild_token_1: str):
    # initially there are no publishers.
    async with engine.begin() as conn:
        assert (await get_all_publishers(conn)) == []

    resp = await client.post("/publisher/new/discord", json={
        "publisher_name": "test publisher"
    }, headers={
        "authorization": f"Bearer {discord_guild_token_1}"
    })

    resp.raise_for_status()

    # there is now one publisher.
    async with engine.begin() as conn:
        publishers = await get_all_publishers(conn)
        assert len(publishers) == 1
        publisher = publishers[0]
        assert publisher.id is not None
        assert publisher.cutoff is not None
        
        # ...and there is one discord guild credential.
        cred = await get_disc_guild_credential("discord_guild_id", conn)
        assert cred.publisher_id == publisher.id

@pytest.mark.asyncio
async def test_publisher_new_returns_409_if_discord_guild_credential_already_exists(
    client: AsyncClient,
    discord_guild_token_1: str
):
    # this is just from before.
    resp = await client.post("/publisher/new/discord", json={
        "publisher_name": "test publisher"
    }, headers={
        "authorization": f"Bearer {discord_guild_token_1}"
    })
    resp.raise_for_status()

    # now if I fire it again...
    resp = await client.post("/publisher/new/discord", json={
        "publisher_name": "test publisher"
    }, headers={
        "authorization": f"Bearer {discord_guild_token_1}"
    })
    assert resp.status_code == 409
    assert resp.json() == {
        "error_code": "DiscordGuildCredentialAlreadyExists",
        "message": "Discord guild credential discord_guild_id already is linked to a publisher.",
        "extra_data": {
            "credential_id": "discord_guild_id"
        }
    }

@pytest.mark.asyncio
async def test_publisher_new_returns_422_if_incorrect_parameters_are_given(
    client: AsyncClient,
    discord_guild_token_1: str
):
    resp = await client.post("/publisher/new/discord", json={
        "publisher_namae": "test publisher"
    }, headers={
        "authorization": f"Bearer {discord_guild_token_1}"
    })
    assert resp.status_code == 422
    assert resp.json() == {
        "error_code": "BodyValidationError",
        "message": "Object missing required field `publisher_name`"
    }
