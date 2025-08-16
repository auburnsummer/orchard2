from django.core.exceptions import PermissionDenied
from django.test import Client
from django.core.signing import TimestampSigner
import pytest
from freezegun import freeze_time

good_signer = TimestampSigner(salt="connectgroup")
bad_signer = TimestampSigner(salt="lalalalalala")

@pytest.mark.django_db
def test_connect_discord_get_returns_no_result_on_invalid_code(bridge_client, user_with_buncha_clubs):
    bridge_client.force_login(user_with_buncha_clubs)
    response = bridge_client.get('/groups/connect_discord/aaaaa/')
    
    assert response.json()['props']['guild_id'] is None

@pytest.mark.django_db
def test_connect_discord_get_returns_no_result_on_different_salt_code(bridge_client, user_with_buncha_clubs):
    bridge_client.force_login(user_with_buncha_clubs)
    token = bad_signer.sign("hello_guild_id")
    response = bridge_client.get(f'/groups/connect_discord/{token}/')

    assert response.json()['props']['guild_id'] is None

@pytest.mark.django_db
def test_connect_discord_post_errors_on_invalid_code(bridge_client, user_with_buncha_clubs):
    bridge_client.force_login(user_with_buncha_clubs)
    response = bridge_client.post('/groups/connect_discord/aaaaa/')
    assert response.status_code == 403

@pytest.mark.django_db
def test_connect_discord_post_errors_on_different_salt_code(bridge_client, user_with_buncha_clubs):
    bridge_client.force_login(user_with_buncha_clubs)
    token = bad_signer.sign("hello_guild_id")
    response = bridge_client.post(f'/groups/connect_discord/{token}/')
    assert response.status_code == 403

@pytest.mark.django_db
def test_connect_discord_get_returns_owned_clubs_and_existing_guild(bridge_client, user_with_buncha_clubs):
    bridge_client.force_login(user_with_buncha_clubs)
    token = good_signer.sign("hello_guild_id")
    response = bridge_client.get(f'/groups/connect_discord/{token}/')

    body = response.json()

    assert body['props']['guild_id'] == "hello_guild_id"
    # does not contain clubb because user_with_buncha_clubs does not own it
    assert body['props']['clubs'] == [
        {
            'id': 'ca',
            'name': 'cluba'
        }
    ]

@pytest.mark.django_db
def test_connect_discord_post_connects_the_club(bridge_client, user_with_buncha_clubs):
    bridge_client.force_login(user_with_buncha_clubs)
    token = good_signer.sign("hello_guild_id")
    response = bridge_client.post(f'/groups/connect_discord/{token}/', {
        "club_id": "ca"
    })
    assert response.status_code == 200

    from cafe.models.discord_guild import DiscordGuild
    dg = DiscordGuild.objects.get(id="hello_guild_id")
    assert dg.club.id == "ca"

@pytest.mark.django_db
def test_connect_discord_post_errors_on_connecting_to_non_owned_club(bridge_client, user_with_buncha_clubs):
    bridge_client.force_login(user_with_buncha_clubs)
    token = good_signer.sign("hello_guild_id")
    response = bridge_client.post(f'/groups/connect_discord/{token}/', {
        "club_id": "cb"  # user_with_buncha_clubs does not own this club
    })
    
    assert response.status_code == 403

@pytest.mark.django_db
def test_connect_discord_post_errors_if_code_too_old(bridge_client, user_with_buncha_clubs):
    bridge_client.force_login(user_with_buncha_clubs)
    with freeze_time("2023-10-01"):
        token = good_signer.sign("hello_guild_id")
    with freeze_time("2023-10-05"):
        response = bridge_client.post(f'/groups/connect_discord/{token}/', {
            "club_id": "ca"
        })
    assert response.status_code == 403