from django.test import Client
from cafe.models.user import User
import pytest

def test_profile_clubs_does_not_allow_anonymous(client: Client):
    # nb: the bridge_client would return a 200 with a "redirect" type
    # we could test that, but ehh
    response = client.get('/accounts/profile/groups/')
    assert response.status_code == 302
    assert response.url == '/accounts/login/?next=/accounts/profile/groups/'

@pytest.mark.django_db
def test_profile_clubs_with_clubless_user(bridge_client: Client, user_with_no_clubs: User):
    bridge_client.force_login(user_with_no_clubs)
    response = bridge_client.get('/accounts/profile/groups/')
    assert response.status_code == 200
    assert response.json()['props'] == {
        'clubs': []
    }

@pytest.mark.django_db
def test_profile_clubs_with_user_with_clubs(bridge_client: Client, user_with_buncha_clubs: User):
    bridge_client.force_login(user_with_buncha_clubs)
    response = bridge_client.get('/accounts/profile/groups/')
    assert response.status_code == 200
    clubs = response.json()['props']['clubs']
    assert len(clubs) == 2
    assert clubs == [
        {
            'club': {
                'id': 'ca',
                'name': 'cluba',
            },
            'role': 'owner',
        },
        {
            'club': {
                'id': 'cb',
                'name': 'clubb',
            },
            'role': 'admin',
        },
    ]