from httpx import AsyncClient, HTTPStatusError
from orchard.projects.v1.core.auth import AssetURLScope, OrchardAuthScopes, PublisherAddScope, make_token_now
from orchard.projects.v1.models.engine import select
from orchard.projects.v1.models.publishers import Publisher
from orchard.projects.v1.models.rd_levels import RDLevel
from orchard.projects.v1.models.users import User
import pytest
import msgspec

from datetime import datetime, timedelta

@pytest.mark.asyncio
async def test_create_rdlevel_happy_path(client: AsyncClient, mock_user: User, mock_publisher: Publisher):
    test_payload = {
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

    url_scope = {
        "image": "https://example.com/testimage.png",
        "thumb": "https://example.com/testimage-thumb.png",
        "url": "https://example.com/testlevel.rdzip",
        "sha1": "testsha1",
        "rdlevel_sha1": "testrdlevelsha1",
        "is_animated": True
    }
    url_scope = msgspec.convert(url_scope, type=AssetURLScope)

    publisher_add_scope = {
        "publisher_id": mock_publisher.id,
        "user_id": mock_user.id,
        "url": "https://example.com/testlevel.rdzip"
    }
    publisher_add_scope = msgspec.convert(publisher_add_scope, type=PublisherAddScope)

    token = make_token_now(scopes=OrchardAuthScopes(
        Publisher_add=publisher_add_scope,
        Publisher_prefill=url_scope
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
    assert the_level.sha1 == url_scope.sha1