from httpx import AsyncClient
from orchard.projects.v1.core.auth import OrchardAuthScopes, make_token_now
from orchard.projects.v1.models.discord_guild_credentials import DiscordGuildPublisherCredential
from orchard.projects.v1.models.engine import select
from orchard.projects.v1.models.publishers import Publisher
# from orchard.projects.v1.models.discord_guild_credentials import get_disc_guild_credential
# from orchard.projects.v1.models.publishers import get_all_publishers
# from orchard.projects.v1.models.metadata import engine
import pytest
from datetime import timedelta

@pytest.fixture
def discord_guild_token_1():
    return make_token_now(
        scopes=OrchardAuthScopes(
            DiscordGuild_register="discord_guild_id"
        ),
        exp_time=timedelta(days=1)
    )

@pytest.mark.asyncio
async def test_publisher_new_creates_a_new_publisher_and_credential(client: AsyncClient, discord_guild_token_1: str):
    # initially there are no publishers.
    publishers = list(select(Publisher).all())
    assert publishers == []

    resp = await client.post("/publisher/new/discord", json={
        "publisher_name": "test publisher"
    }, headers={
        "authorization": f"Bearer {discord_guild_token_1}"
    })

    resp.raise_for_status()

    # there is now one publisher.
    publishers = list(select(Publisher).all())
    assert len(publishers) == 1
    publisher = publishers[0]
    assert publisher.id is not None
    assert publisher.name == "test publisher"

    # ...and there is one discord guild credential.
    dgcs = list(select(DiscordGuildPublisherCredential).all())
    assert len(dgcs) == 1
    assert dgcs[0].publisher == publisher

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

# @pytest.mark.skip
# @pytest.mark.asyncio
# async def test_publisher_new_returns_422_if_incorrect_parameters_are_given(
#     client: AsyncClient,
#     discord_guild_token_1: str
# ):
#     resp = await client.post("/publisher/new/discord", json={
#         "publisher_namae": "test publisher"
#     }, headers={
#         "authorization": f"Bearer {discord_guild_token_1}"
#     })
#     assert resp.status_code == 422
#     assert resp.json() == {
#         "error_code": "BodyValidationError",
#         "message": "Object missing required field `publisher_name`"
#     }
