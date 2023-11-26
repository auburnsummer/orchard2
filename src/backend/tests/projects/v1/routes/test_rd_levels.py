from httpx import AsyncClient, HTTPStatusError
from orchard.projects.v1.core.auth import OrchardAuthScopes, PublisherAddAssetsScope, PublisherRDPrefillScope, make_token_now
from orchard.projects.v1.models.engine import select
from orchard.projects.v1.models.publishers import Publisher
from orchard.projects.v1.models.rd_levels import RDLevel
from orchard.projects.v1.models.users import User
import pytest
import msgspec

from datetime import datetime, timedelta

@pytest.fixture
def test_payload():
    return {
        "artist": "shino ft. Hatsune Miku",
        "artist_tokens": ["shino", "Hatsune Miku"],
        "song": "花を唄う",
        "song_alt": "Singing of a flower",
        "seizure_warning": False,
        "description": "friendship ended with vflower now miku is my best friend",
        "hue": 0.4,
        "authors": ["auburnsummer", "labyrinth"],
        "authors_raw": "auburnsummer,labyrinth",
        "max_bpm": 115,
        "min_bpm": 115,
        "difficulty": 2,
        "single_player": True,
        "two_player": False,
        "last_updated": datetime.fromtimestamp(1650269435).isoformat(),
        "tags": ["vocaloid","project sekai"],
        "has_classics": True,
        "has_oneshots": True,
        "has_squareshots": False,
        "has_freezeshots": False,
        "has_freetimes": False,
        "has_holds": False,
        "has_skipshots": True,
        "has_window_dance": False
    }

@pytest.fixture
def publisher_assets_scope():
    url_scope = {
        "image": "https://cabinet.rhythm.cafe/testimage.png",
        "thumb": "https://cabinet.rhythm.cafe/testimage-thumb.png",
        "url": "https://cabinet.rhythm.cafe/testlevel.rdzip",
        "sha1": "testsha1",
        "rdlevel_sha1": "testrdlevelsha1",
        "is_animated": True,
        "link_id": "testlinkid"
    }
    return msgspec.convert(url_scope, type=PublisherAddAssetsScope)

@pytest.fixture
def publisher_prefill_scope(
    mock_user: User,
    mock_publisher: Publisher
):
    rd_prefill_scope = {
        "publisher_id": mock_publisher.id,
        "user_id": mock_user.id,
        "url": "https://third.party.website/testlevel.rdzip",
        "link_id": "testlinkid"
    }
    rd_prefill_scope = msgspec.convert(rd_prefill_scope, type=PublisherRDPrefillScope)
    return rd_prefill_scope


@pytest.mark.asyncio
async def test_create_rdlevel_happy_path(
    client: AsyncClient,
    mock_user: User,
    mock_publisher: Publisher,
    test_payload,
    publisher_assets_scope,
    publisher_prefill_scope
):


    token = make_token_now(scopes=OrchardAuthScopes(
        Publisher_rdadd=publisher_assets_scope,
        Publisher_rdprefill=publisher_prefill_scope
    ), exp_time=timedelta(hours=1))

    resp = await client.post("/rdlevel", headers={
        "authorization": f"Bearer {token}"
    }, json={
        "level": test_payload
    })
    try:
        resp.raise_for_status()
    except HTTPStatusError as err:
        print(resp.content)
        raise err

    id = resp.json()["level"]["id"]

    # there should now be one level in the db.
    the_level = select(RDLevel).by_id(id)

    assert the_level.id == id
    assert the_level.song == test_payload["song"]
    assert the_level.song_alt == test_payload["song_alt"]
    assert the_level.sha1 == publisher_assets_scope.sha1


@pytest.mark.asyncio
async def test_throws_error_if_url_from_prefill_and_add_dont_match(
    client: AsyncClient,
    mock_user: User,
    mock_publisher: Publisher,
    test_payload,
    publisher_assets_scope,
    publisher_prefill_scope
):
    publisher_assets_scope.link_id = "ahiwofekawefhawelfk"
    token = make_token_now(scopes=OrchardAuthScopes(
        Publisher_rdadd=publisher_assets_scope,
        Publisher_rdprefill=publisher_prefill_scope
    ), exp_time=timedelta(hours=1))

    resp = await client.post("/rdlevel", headers={
        "authorization": f"Bearer {token}"
    }, json={
        "level": test_payload
    })
    assert resp.status_code == 403
    assert resp.json() ==          {'error_code': 'LinkedTokensIDMismatch',
          'message': 'adding rd level: received mismatching ids ahiwofekawefhawelfk and '
                    'testlinkid. Try the command from the start. If you see this '
                     "again, it's a bug, ping auburn"}