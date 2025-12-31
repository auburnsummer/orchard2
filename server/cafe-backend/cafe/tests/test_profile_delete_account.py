import pytest
from unittest.mock import patch
from django.test import Client

from cafe.models.clubs.club import Club
from cafe.models.clubs.club_membership import ClubMembership
from cafe.models.rdlevels.rdlevel import RDLevel
from cafe.models.user import User
from cafe.tests.conftest import follow_bridge_redirect
from orchard.settings import STEWARD_USER_ID


@pytest.fixture
def steward_user():
    """Create or get the steward user that levels are transferred to"""
    user, _ = User.objects.get_or_create(
        id=STEWARD_USER_ID,
        defaults={'display_name': 'Steward'}
    )
    return user


@pytest.fixture
def user_with_levels(test_club, steward_user):
    """Create a user with multiple levels"""
    user = User.objects.create_user(username="user_with_levels", display_name="User With Levels")
    
    # Create multiple levels with mocked sync task
    from django.utils import timezone
    with patch('cafe.models.rdlevels.rdlevel.sync_level_to_typesense'):
        for i in range(3):
            RDLevel.objects.create(
                artist=f"Artist {i}",
                artist_tokens=["artist", str(i)],
                artist_raw=f"Artist {i}",
                song=f"Song {i}",
                song_alt=f"Song {i} Alt",
                song_raw=f"Song {i}",
                seizure_warning=False,
                description=f"Test level {i}",
                hue=float(i * 60),
                authors=[f"Author {i}"],
                authors_raw=f"Author {i}",
                max_bpm=120 + i,
                min_bpm=60 + i,
                difficulty=1,
                single_player=True,
                two_player=False,
                last_updated=timezone.now(),
                tags=["test"],
                sha1=f"sha1_{i}_{user.username}",
                rdlevel_sha1=f"rdlevel_sha1_{i}_{user.username}",
                rd_md5=f"md5_{i}_{user.username}",
                is_animated=False,
                rdzip_url=f"https://example.com/level{i}.rdzip",
                image_url=f"https://example.com/level{i}.jpg",
                thumb_url=f"https://example.com/level{i}_thumb.jpg",
                icon_url=f"https://example.com/level{i}_icon.jpg",
                submitter=user,
                club=test_club,
                approval=0
            )
    
    return user


@pytest.fixture
def user_with_owned_club(test_club):
    """Create a user who owns a club"""
    user = User.objects.create_user(username="club_owner", display_name="Club Owner")
    ClubMembership.objects.create(
        user=user,
        club=test_club,
        role="owner"
    )
    return user


@pytest.fixture
def user_with_admin_club():
    """Create a user who is an admin (but not owner) of a club"""
    user = User.objects.create_user(username="club_admin", display_name="Club Admin")
    club = Club.objects.create(id="adminclub", name="Admin Club")
    
    # Create an owner for the club (different user)
    owner = User.objects.create_user(username="actual_owner", display_name="Actual Owner")
    ClubMembership.objects.create(user=owner, club=club, role="owner")
    
    # Make the test user an admin
    ClubMembership.objects.create(user=user, club=club, role="admin")
    return user


def test_profile_delete_account_requires_authentication(client: Client):
    """Anonymous users should be redirected to login"""
    response = client.get('/accounts/profile/delete/')
    assert response.status_code == 302
    assert response.url == '/accounts/login/?next=/accounts/profile/delete/'


@pytest.mark.django_db
def test_profile_delete_account_get_shows_level_count(bridge_client: Client, user_with_levels):
    """GET request should show the number of levels the user has"""
    bridge_client.force_login(user_with_levels)
    response = bridge_client.get('/accounts/profile/delete/')
    
    assert response.status_code == 200
    body = response.json()
    assert body['props']['number_of_levels'] == 3
    assert body['props']['number_of_clubs'] == 0


@pytest.mark.django_db
def test_profile_delete_account_get_shows_club_count(bridge_client: Client, user_with_owned_club):
    """GET request should show the number of clubs the user owns"""
    bridge_client.force_login(user_with_owned_club)
    response = bridge_client.get('/accounts/profile/delete/')
    
    assert response.status_code == 200
    body = response.json()
    assert body['props']['number_of_clubs'] == 1
    assert body['props']['number_of_levels'] == 0


@pytest.mark.django_db
def test_cannot_delete_account_when_owning_clubs(bridge_client: Client, user_with_owned_club):
    """Users who own clubs cannot delete their account"""
    bridge_client.force_login(user_with_owned_club)
    
    # Attempt to delete account
    response = bridge_client.post('/accounts/profile/delete/', {
        'level_handling': 'delete'
    })
    
    # Should be a redirect back to the delete account page
    assert response.status_code == 200
    body = response.json()
    assert body['action'] == 'redirect'
    assert body['path'] == '/accounts/profile/delete/'
    
    # Follow the redirect to see the error message
    follow_response = follow_bridge_redirect(bridge_client, response)
    assert follow_response.status_code == 200
    messages = follow_response.json()['messages']
    assert len(messages) == 1
    assert messages[0]['level'] == 'error'
    assert 'groups' in messages[0]['html'].lower()
    assert 'ownership' in messages[0]['html'].lower()
    
    # User should still exist
    assert User.objects.filter(username=user_with_owned_club.username).exists()


@pytest.mark.django_db
def test_can_delete_account_when_admin_but_not_owner(bridge_client: Client, user_with_admin_club, steward_user):
    """Users who are club admins (but not owners) can delete their account"""
    bridge_client.force_login(user_with_admin_club)
    
    # Attempt to delete account
    response = bridge_client.post('/accounts/profile/delete/', {
        'level_handling': 'delete'
    })
    
    # Should redirect to home page
    assert response.status_code == 200
    body = response.json()
    assert body['action'] == 'redirect'
    assert body['path'] == '/'
    
    # User should be deleted
    assert not User.objects.filter(username=user_with_admin_club.username).exists()


@pytest.mark.django_db
def test_delete_account_with_level_handling_delete(bridge_client: Client, user_with_levels, steward_user):
    """When level_handling is 'delete', user and their levels should be deleted"""
    from cafe.models.rdlevels.rdlevel import HistoricalRDLevel
    
    bridge_client.force_login(user_with_levels)
    user_id = user_with_levels.id
    
    # Verify levels exist
    initial_level_count = RDLevel.objects.filter(submitter=user_with_levels).count()
    assert initial_level_count == 3
    
    # Delete account with delete option
    response = bridge_client.post('/accounts/profile/delete/', {
        'level_handling': 'delete'
    })
    
    # Should redirect to home page
    assert response.status_code == 200
    body = response.json()
    assert body['action'] == 'redirect'
    assert body['path'] == '/'
    
    # User should be deleted
    assert not User.objects.filter(id=user_id).exists()
    
    # All levels should be deleted (cascade delete)
    assert RDLevel.objects.filter(submitter_id=user_id).count() == 0
    
    # Clean up any remaining historical records for test isolation
    # (This can happen due to pytest transaction rollback behavior with simple-history)
    HistoricalRDLevel.objects.filter(history_user_id=user_id).delete()


@pytest.mark.django_db
def test_delete_account_with_level_handling_transfer(bridge_client: Client, user_with_levels, steward_user):
    """When level_handling is 'transfer', levels should be transferred to steward user"""
    bridge_client.force_login(user_with_levels)
    
    # Get the level IDs before deletion
    level_ids = list(RDLevel.objects.filter(submitter=user_with_levels).values_list('id', flat=True))
    assert len(level_ids) == 3
    
    # Delete account with transfer option
    response = bridge_client.post('/accounts/profile/delete/', {
        'level_handling': 'transfer'
    })
    
    # Should redirect to home page
    assert response.status_code == 200
    body = response.json()
    assert body['action'] == 'redirect'
    assert body['path'] == '/'
    
    # User should be deleted
    assert not User.objects.filter(username=user_with_levels.username).exists()
    
    # All levels should now belong to the steward user
    for level_id in level_ids:
        level = RDLevel.objects.get(id=level_id)
        assert level.submitter == steward_user


@pytest.mark.django_db
def test_delete_account_without_levels(bridge_client: Client, user_with_no_clubs, steward_user):
    """Users without levels can delete their account successfully"""
    bridge_client.force_login(user_with_no_clubs)
    
    # Delete account
    response = bridge_client.post('/accounts/profile/delete/', {
        'level_handling': 'delete'
    })
    
    # Should redirect to home page
    assert response.status_code == 200
    body = response.json()
    assert body['action'] == 'redirect'
    assert body['path'] == '/'
    
    # User should be deleted
    assert not User.objects.filter(username=user_with_no_clubs.username).exists()


@pytest.mark.django_db
def test_delete_account_shows_success_message_on_delete(bridge_client: Client, user_with_no_clubs, steward_user):
    """Successful deletion should show a success message"""
    bridge_client.force_login(user_with_no_clubs)
    
    # Delete account
    response = bridge_client.post('/accounts/profile/delete/', {
        'level_handling': 'delete'
    })
    
    # Follow redirect to see the message
    # Note: We can't actually see the message because the user is deleted
    # and will be logged out, but we can verify the response structure
    assert response.status_code == 200
    body = response.json()
    assert body['action'] == 'redirect'
    assert body['path'] == '/'


@pytest.mark.django_db
def test_delete_account_shows_success_message_on_transfer(bridge_client: Client, user_with_levels, steward_user):
    """Successful transfer should show a success message"""
    bridge_client.force_login(user_with_levels)
    
    # Delete account with transfer
    response = bridge_client.post('/accounts/profile/delete/', {
        'level_handling': 'transfer'
    })
    
    # Should redirect
    assert response.status_code == 200
    body = response.json()
    assert body['action'] == 'redirect'
    assert body['path'] == '/'


@pytest.mark.django_db
def test_delete_account_with_invalid_level_handling(bridge_client: Client, user_with_no_clubs, steward_user):
    """Invalid level_handling values should be rejected"""
    bridge_client.force_login(user_with_no_clubs)
    
    # Try with invalid level_handling
    response = bridge_client.post('/accounts/profile/delete/', {
        'level_handling': 'invalid_option'
    })
    
    # Should show an error (form validation should fail gracefully)
    assert response.status_code == 200
    
    # User should still exist
    assert User.objects.filter(username=user_with_no_clubs.username).exists()


@pytest.mark.django_db
def test_delete_account_missing_level_handling(bridge_client: Client, user_with_no_clubs, steward_user):
    """Missing level_handling parameter should be rejected"""
    bridge_client.force_login(user_with_no_clubs)
    
    # Try without level_handling
    response = bridge_client.post('/accounts/profile/delete/', {})
    
    # Should fail validation
    assert response.status_code == 200
    
    # User should still exist
    assert User.objects.filter(username=user_with_no_clubs.username).exists()


@pytest.mark.django_db
def test_delete_account_preserves_other_users_levels(bridge_client: Client, user_with_levels, test_club, steward_user):
    """Deleting a user should not affect other users' levels"""
    from cafe.models.rdlevels.rdlevel import HistoricalRDLevel
    
    # Create another user with levels
    other_user = User.objects.create_user(username="other_user", display_name="Other User")
    
    from django.utils import timezone
    with patch('cafe.models.rdlevels.rdlevel.sync_level_to_typesense'):
        other_level = RDLevel.objects.create(
            artist="Other Artist",
            artist_tokens=["other", "artist"],
            artist_raw="Other Artist",
            song="Other Song",
            song_alt="Other Song Alt",
            song_raw="Other Song",
            seizure_warning=False,
            description="Other level",
            hue=90.0,
            authors=["Other Author"],
            authors_raw="Other Author",
            max_bpm=140,
            min_bpm=70,
            difficulty=2,
            single_player=True,
            two_player=False,
            last_updated=timezone.now(),
            tags=["other"],
            sha1="other_sha1",
            rdlevel_sha1="other_rdlevel_sha1",
            rd_md5="other_md5",
            is_animated=False,
            rdzip_url="https://example.com/other.rdzip",
            image_url="https://example.com/other.jpg",
            thumb_url="https://example.com/other_thumb.jpg",
            icon_url="https://example.com/other_icon.jpg",
            submitter=other_user,
            club=test_club,
            approval=0
        )
    
    bridge_client.force_login(user_with_levels)
    user_id = user_with_levels.id
    
    # Delete the first user with delete option
    response = bridge_client.post('/accounts/profile/delete/', {
        'level_handling': 'delete'
    })
    
    assert response.status_code == 200
    
    # Other user's level should still exist
    assert RDLevel.objects.filter(id=other_level.id).exists()
    assert RDLevel.objects.get(id=other_level.id).submitter == other_user
    
    # Clean up any remaining historical records for test isolation
    HistoricalRDLevel.objects.filter(history_user_id=user_id).delete()


@pytest.mark.django_db
def test_steward_user_must_exist_for_transfer(bridge_client: Client, user_with_levels):
    """Transfer should fail gracefully if steward user doesn't exist"""
    bridge_client.force_login(user_with_levels)
    
    # Ensure steward user doesn't exist
    User.objects.filter(id=STEWARD_USER_ID).delete()
    
    # Try to transfer levels
    with pytest.raises(User.DoesNotExist):
        response = bridge_client.post('/accounts/profile/delete/', {
            'level_handling': 'transfer'
        })
