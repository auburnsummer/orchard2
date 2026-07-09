import pytest
from unittest.mock import patch
from django.utils import timezone

from cafe.models.clubs.club import Club
from cafe.models.clubs.club_membership import ClubMembership
from cafe.models.rdlevels.rdlevel import RDLevel
from cafe.models.user import User


@pytest.fixture
def pharmacy_club():
    """Create the pharmacy club (cpharmacy)"""
    return Club.objects.create(id="cpharmacy", name="Pharmacy")


@pytest.fixture
def pharmacist_user(pharmacy_club):
    """Create a user who is an admin of the pharmacy club (a pharmacist)"""
    user = User.objects.create_user(username="pharmacist_user", display_name="Pharmacist User")
    ClubMembership.objects.create(
        user=user,
        club=pharmacy_club,
        role="admin"
    )
    return user


@pytest.fixture
def regular_user():
    """A user with no special permissions"""
    return User.objects.create_user(username="regular_user", display_name="Regular User")


@pytest.fixture
def new_submitter():
    """The user levels will be transferred to"""
    return User.objects.create_user(username="new_submitter", display_name="New Submitter")


@pytest.fixture
def original_submitter():
    """The user levels initially belong to"""
    return User.objects.create_user(username="original_submitter", display_name="Original Submitter")


@pytest.fixture
def test_club():
    return Club.objects.create(id="testclub", name="Test Club")


def create_level(submitter, club, suffix):
    """Helper to create an RDLevel owned by `submitter`, without hitting typesense."""
    with patch('cafe.models.rdlevels.rdlevel.sync_level_to_typesense'):
        return RDLevel.objects.create(
            artist=f"Artist {suffix}",
            artist_tokens=["artist", str(suffix)],
            artist_raw=f"Artist {suffix}",
            song=f"Song {suffix}",
            song_alt=f"Song {suffix} Alt",
            song_raw=f"Song {suffix}",
            seizure_warning=False,
            description=f"Test level {suffix}",
            hue=float(suffix % 360),
            authors=["Test Author"],
            authors_raw="Test Author",
            max_bpm=120,
            min_bpm=60,
            difficulty=1,
            single_player=True,
            two_player=False,
            last_updated=timezone.now(),
            tags=["test"],
            sha1=f"sha1_{suffix}",
            rdlevel_sha1=f"rdlevel_sha1_{suffix}",
            rd_md5=f"md5_{suffix}",
            is_animated=False,
            rdzip_url=f"https://example.com/level{suffix}.rdzip",
            image_url=f"https://example.com/image{suffix}.jpg",
            thumb_url=f"https://example.com/thumb{suffix}.jpg",
            icon_url=f"https://example.com/icon{suffix}.jpg",
            submitter=submitter,
            club=club,
            approval=0
        )


@pytest.fixture
def level(original_submitter, test_club):
    return create_level(original_submitter, test_club, 1)


@pytest.fixture
def levels(original_submitter, test_club):
    return [create_level(original_submitter, test_club, i) for i in range(3)]


# GET request tests


@pytest.mark.django_db
def test_pharmacist_can_access_bulk_transfer_page(bridge_client, pharmacist_user):
    """Pharmacists should be able to access the bulk transfer page"""
    bridge_client.force_login(pharmacist_user)
    response = bridge_client.get('/pharmacy/bulk-transfer/')

    assert response.status_code == 200
    body = response.json()
    assert body['action'] == 'render'


@pytest.mark.django_db
def test_non_pharmacist_cannot_access_bulk_transfer_page(bridge_client, regular_user):
    """Non-pharmacists should not be able to access the bulk transfer page"""
    bridge_client.force_login(regular_user)
    response = bridge_client.get('/pharmacy/bulk-transfer/')

    assert response.status_code == 200
    body = response.json()
    assert body['action'] == 'redirect'


@pytest.mark.django_db
def test_anonymous_user_cannot_access_bulk_transfer_page(bridge_client):
    """Anonymous users should be redirected away from the bulk transfer page"""
    response = bridge_client.get('/pharmacy/bulk-transfer/')

    assert response.status_code == 200
    body = response.json()
    assert body['action'] == 'redirect'


# POST request tests - success cases


@pytest.mark.django_db
@patch('cafe.models.rdlevels.rdlevel.sync_level_to_typesense')
def test_bulk_transfer_moves_single_level(mock_sync, bridge_client, pharmacist_user, level, new_submitter):
    """A single level should be transferred to the new submitter"""
    bridge_client.force_login(pharmacist_user)

    response = bridge_client.post('/pharmacy/bulk-transfer/', {
        'level_ids': str(level.id),
        'user_id': str(new_submitter.id),
    })

    assert response.status_code == 200
    level.refresh_from_db()
    assert level.submitter_id == new_submitter.id

    body = response.json()
    assert len(body['messages']) == 1
    assert body['messages'][0]['level'] == 'success'
    assert 'Transferred 1 levels' in body['messages'][0]['html']
    assert new_submitter.display_name in body['messages'][0]['html']


@pytest.mark.django_db
@patch('cafe.models.rdlevels.rdlevel.sync_level_to_typesense')
def test_bulk_transfer_moves_multiple_levels(mock_sync, bridge_client, pharmacist_user, levels, new_submitter):
    """Multiple levels (newline separated ids) should all be transferred"""
    bridge_client.force_login(pharmacist_user)

    level_ids = "\n".join(str(level.id) for level in levels)
    response = bridge_client.post('/pharmacy/bulk-transfer/', {
        'level_ids': level_ids,
        'user_id': str(new_submitter.id),
    })

    assert response.status_code == 200
    for level in levels:
        level.refresh_from_db()
        assert level.submitter_id == new_submitter.id

    body = response.json()
    assert 'Transferred 3 levels' in body['messages'][0]['html']


@pytest.mark.django_db
@patch('cafe.models.rdlevels.rdlevel.sync_level_to_typesense')
def test_bulk_transfer_ignores_nonexistent_level_ids(mock_sync, bridge_client, pharmacist_user, level, new_submitter):
    """Nonexistent level ids in the list should be silently ignored"""
    bridge_client.force_login(pharmacist_user)

    level_ids = f"{level.id}\nnonexistent-id"
    response = bridge_client.post('/pharmacy/bulk-transfer/', {
        'level_ids': level_ids,
        'user_id': str(new_submitter.id),
    })

    assert response.status_code == 200
    level.refresh_from_db()
    assert level.submitter_id == new_submitter.id

    body = response.json()
    assert 'Transferred 1 levels' in body['messages'][0]['html']


# POST request tests - failure cases


@pytest.mark.django_db
def test_bulk_transfer_with_nonexistent_user_shows_error(bridge_client, pharmacist_user, level):
    """If the target user doesn't exist, an error message is shown and nothing is transferred"""
    bridge_client.force_login(pharmacist_user)
    original_submitter_id = level.submitter_id

    response = bridge_client.post('/pharmacy/bulk-transfer/', {
        'level_ids': str(level.id),
        'user_id': '999999',
    })

    assert response.status_code == 200
    level.refresh_from_db()
    assert level.submitter_id == original_submitter_id

    body = response.json()
    assert len(body['messages']) == 1
    assert body['messages'][0]['level'] == 'error'
    assert 'User does not exist' in body['messages'][0]['html']


@pytest.mark.django_db
def test_bulk_transfer_with_missing_user_id_is_invalid(bridge_client, pharmacist_user, level):
    """Omitting user_id should be treated as an invalid form submission"""
    bridge_client.force_login(pharmacist_user)
    original_submitter_id = level.submitter_id

    response = bridge_client.post('/pharmacy/bulk-transfer/', {
        'level_ids': str(level.id),
    })

    assert response.status_code == 200
    level.refresh_from_db()
    assert level.submitter_id == original_submitter_id

    body = response.json()
    assert len(body['messages']) == 1
    assert 'Invalid form submission' in body['messages'][0]['html']


@pytest.mark.django_db
def test_bulk_transfer_with_missing_level_ids_is_invalid(bridge_client, pharmacist_user, new_submitter):
    """Omitting level_ids should be treated as an invalid form submission"""
    bridge_client.force_login(pharmacist_user)

    response = bridge_client.post('/pharmacy/bulk-transfer/', {
        'user_id': str(new_submitter.id),
    })

    assert response.status_code == 200
    body = response.json()
    assert len(body['messages']) == 1
    assert 'Invalid form submission' in body['messages'][0]['html']


@pytest.mark.django_db
def test_non_pharmacist_cannot_bulk_transfer(bridge_client, regular_user, level, new_submitter):
    """Non-pharmacists should not be able to perform a bulk transfer"""
    bridge_client.force_login(regular_user)
    original_submitter_id = level.submitter_id

    response = bridge_client.post('/pharmacy/bulk-transfer/', {
        'level_ids': str(level.id),
        'user_id': str(new_submitter.id),
    })

    assert response.status_code == 200
    body = response.json()
    assert body['action'] == 'redirect'

    # Nothing should have been transferred
    level.refresh_from_db()
    assert level.submitter_id == original_submitter_id


@pytest.mark.django_db
def test_anonymous_user_cannot_bulk_transfer(bridge_client, level, new_submitter):
    """Anonymous users should not be able to perform a bulk transfer"""
    original_submitter_id = level.submitter_id

    response = bridge_client.post('/pharmacy/bulk-transfer/', {
        'level_ids': str(level.id),
        'user_id': str(new_submitter.id),
    })

    assert response.status_code == 200
    body = response.json()
    assert body['action'] == 'redirect'

    level.refresh_from_db()
    assert level.submitter_id == original_submitter_id
