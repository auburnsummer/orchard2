import pytest
from unittest.mock import patch
from django.contrib.auth.models import AnonymousUser

from cafe.models.clubs.club import Club
from cafe.models.clubs.club_membership import ClubMembership
from cafe.models.rdlevels.rdlevel import RDLevel
from cafe.models.user import User
from cafe.tests.conftest import follow_bridge_redirect
from orchard.settings import STEWARD_CLUB_ID


@pytest.fixture
def club_owner():
    """Create a user who will be the owner of a club"""
    return User.objects.create_user(username="club_owner", display_name="Club Owner")


@pytest.fixture
def deletable_club(club_owner):
    """Create a club that can be deleted"""
    club = Club.objects.create(id="deletable", name="Deletable Club")
    ClubMembership.objects.create(
        user=club_owner,
        club=club,
        role="owner"
    )
    return club


@pytest.fixture
def steward_club():
    """Create or get the steward club that levels are transferred to"""
    club, _ = Club.objects.get_or_create(
        id=STEWARD_CLUB_ID,
        defaults={'name': 'Steward Club'}
    )
    return club


@pytest.fixture
def club_with_levels(club_owner, steward_club):
    """Create a club with multiple levels"""
    club = Club.objects.create(id="clubwithlevels", name="Club With Levels")
    ClubMembership.objects.create(
        user=club_owner,
        club=club,
        role="owner"
    )
    
    submitter = User.objects.create_user(username="level_submitter", display_name="Level Submitter")
    
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
                sha1=f"sha1_{i}",
                rdlevel_sha1=f"rdlevel_sha1_{i}",
                rd_md5=f"md5_{i}",
                is_animated=False,
                rdzip_url=f"https://example.com/level{i}.rdzip",
                image_url=f"https://example.com/image{i}.jpg",
                thumb_url=f"https://example.com/thumb{i}.jpg",
                icon_url=f"https://example.com/icon{i}.jpg",
                submitter=submitter,
                club=club,
                approval=0
            )
    
    return club


# GET request tests


@pytest.mark.django_db
def test_get_club_delete_page_as_owner(bridge_client, club_owner, deletable_club):
    """Owner should be able to access the delete page"""
    bridge_client.force_login(club_owner)
    response = bridge_client.get(f'/groups/{deletable_club.id}/settings/delete/')
    
    assert response.status_code == 200
    body = response.json()
    assert body['action'] == 'render'
    assert body['props']['club']['id'] == deletable_club.id
    assert body['props']['club_level_count'] == 0


@pytest.mark.django_db
def test_get_club_delete_page_shows_level_count(bridge_client, club_owner, club_with_levels):
    """Delete page should show the correct number of levels"""
    bridge_client.force_login(club_owner)
    response = bridge_client.get(f'/groups/{club_with_levels.id}/settings/delete/')
    
    assert response.status_code == 200
    body = response.json()
    assert body['props']['club_level_count'] == 3


@pytest.mark.django_db
def test_get_club_delete_page_requires_permission(bridge_client, user_with_no_clubs, deletable_club):
    """Non-owners should not be able to access the delete page"""
    bridge_client.force_login(user_with_no_clubs)
    response = bridge_client.get(f'/groups/{deletable_club.id}/settings/delete/')
    
    # Should be redirected or forbidden (permission denied by django-rules)
    # When permission is denied, django-rules redirects to login or shows 403
    assert response.status_code in [200, 403]
    if response.status_code == 200:
        # If it's a redirect response, it should redirect away from the delete page
        body = response.json()
        assert body['action'] == 'redirect'


@pytest.mark.django_db
def test_get_club_delete_page_requires_auth(bridge_client, deletable_club):
    """Unauthenticated users should be redirected"""
    response = bridge_client.get(f'/groups/{deletable_club.id}/settings/delete/')
    
    # Should redirect to login
    assert response.status_code == 200
    body = response.json()
    assert body['action'] == 'redirect'


@pytest.mark.django_db
def test_get_club_delete_page_returns_404_for_nonexistent_club(bridge_client, club_owner):
    """Should return 404 for a club that doesn't exist"""
    bridge_client.force_login(club_owner)
    response = bridge_client.get('/groups/nonexistent/settings/delete/')
    
    assert response.status_code == 404


# DELETE option tests (cascade delete)


@pytest.mark.django_db
def test_delete_club_with_delete_option_removes_club(bridge_client, club_owner, deletable_club):
    """Delete option should remove the club"""
    bridge_client.force_login(club_owner)
    
    response = bridge_client.post(
        f'/groups/{deletable_club.id}/settings/delete/',
        {'level_action': 'delete'}
    )
    
    assert response.status_code == 200
    body = response.json()
    assert body['action'] == 'redirect'
    assert body['path'] == '/accounts/profile/groups/'
    
    # Club should be deleted
    assert not Club.objects.filter(id=deletable_club.id).exists()


@pytest.mark.django_db
def test_delete_club_with_delete_option_cascades_to_levels(bridge_client, club_owner, club_with_levels):
    """Delete option should cascade delete all levels"""
    bridge_client.force_login(club_owner)
    club_id = club_with_levels.id
    
    # Verify levels exist before deletion
    assert RDLevel.objects.filter(club=club_with_levels).count() == 3
    
    response = bridge_client.post(
        f'/groups/{club_id}/settings/delete/',
        {'level_action': 'delete'}
    )
    
    assert response.status_code == 200
    body = response.json()
    assert body['action'] == 'redirect'
    
    # Club should be deleted
    assert not Club.objects.filter(id=club_id).exists()
    
    # All levels should be cascade deleted
    assert RDLevel.objects.filter(club_id=club_id).count() == 0


@pytest.mark.django_db
def test_delete_club_shows_success_message(bridge_client, club_owner, deletable_club):
    """Successful deletion should show a success message"""
    bridge_client.force_login(club_owner)
    
    response = bridge_client.post(
        f'/groups/{deletable_club.id}/settings/delete/',
        {'level_action': 'delete'}
    )
    
    # Follow the redirect to see messages
    final_response = follow_bridge_redirect(bridge_client, response)
    body = final_response.json()
    
    assert len(body['messages']) > 0
    assert body['messages'][0]['level'] == 'success'
    assert 'deleted successfully' in body['messages'][0]['html'].lower()


# DISASSOCIATE option tests (transfer to steward)


@pytest.mark.django_db
def test_disassociate_option_transfers_levels_to_steward(bridge_client, club_owner, club_with_levels, steward_club):
    """Disassociate option should transfer levels to steward club"""
    bridge_client.force_login(club_owner)
    club_id = club_with_levels.id
    
    # Get level IDs before deletion
    level_ids = list(RDLevel.objects.filter(club=club_with_levels).values_list('id', flat=True))
    assert len(level_ids) == 3
    
    response = bridge_client.post(
        f'/groups/{club_id}/settings/delete/',
        {'level_action': 'disassociate'}
    )
    
    assert response.status_code == 200
    body = response.json()
    assert body['action'] == 'redirect'
    
    # Club should be deleted
    assert not Club.objects.filter(id=club_id).exists()
    
    # Levels should still exist and be assigned to steward club
    for level_id in level_ids:
        level = RDLevel.objects.get(id=level_id)
        assert level.club_id == STEWARD_CLUB_ID


@pytest.mark.django_db
def test_disassociate_option_deletes_club_after_transfer(bridge_client, club_owner, club_with_levels, steward_club):
    """Disassociate option should delete the club after transferring levels"""
    bridge_client.force_login(club_owner)
    club_id = club_with_levels.id
    
    response = bridge_client.post(
        f'/groups/{club_id}/settings/delete/',
        {'level_action': 'disassociate'}
    )
    
    assert response.status_code == 200
    
    # Club should be deleted
    assert not Club.objects.filter(id=club_id).exists()
    
    # Membership should also be deleted (cascade)
    assert not ClubMembership.objects.filter(club_id=club_id).exists()


@pytest.mark.django_db
def test_disassociate_option_shows_success_message(bridge_client, club_owner, club_with_levels, steward_club):
    """Successful disassociation should show a success message"""
    bridge_client.force_login(club_owner)
    
    response = bridge_client.post(
        f'/groups/{club_with_levels.id}/settings/delete/',
        {'level_action': 'disassociate'}
    )
    
    # Follow the redirect to see messages
    final_response = follow_bridge_redirect(bridge_client, response)
    body = final_response.json()
    
    assert len(body['messages']) > 0
    assert body['messages'][0]['level'] == 'success'
    assert 'deleted successfully' in body['messages'][0]['html'].lower()


# Invalid input tests


@pytest.mark.django_db
def test_invalid_level_action_shows_error(bridge_client, club_owner, deletable_club):
    """Invalid level_action should show an error message"""
    bridge_client.force_login(club_owner)
    
    response = bridge_client.post(
        f'/groups/{deletable_club.id}/settings/delete/',
        {'level_action': 'invalid_option'}
    )
    
    assert response.status_code == 200
    body = response.json()
    assert body['action'] == 'redirect'
    assert f'/groups/{deletable_club.id}/settings/delete/' in body['path']
    
    # Club should NOT be deleted
    assert Club.objects.filter(id=deletable_club.id).exists()
    
    # Follow redirect to see error message
    final_response = follow_bridge_redirect(bridge_client, response)
    body = final_response.json()
    
    assert len(body['messages']) > 0
    assert body['messages'][0]['level'] == 'error'
    assert 'invalid' in body['messages'][0]['html'].lower()


@pytest.mark.django_db
def test_missing_level_action_shows_error(bridge_client, club_owner, deletable_club):
    """Missing level_action should show an error message"""
    bridge_client.force_login(club_owner)
    
    response = bridge_client.post(
        f'/groups/{deletable_club.id}/settings/delete/',
        {}  # No level_action provided
    )
    
    assert response.status_code == 200
    body = response.json()
    assert body['action'] == 'redirect'
    
    # Club should NOT be deleted
    assert Club.objects.filter(id=deletable_club.id).exists()
    
    # Follow redirect to see error message
    final_response = follow_bridge_redirect(bridge_client, response)
    body = final_response.json()
    
    assert len(body['messages']) > 0
    assert body['messages'][0]['level'] == 'error'


# Permission tests


@pytest.mark.django_db
def test_admin_cannot_delete_club(bridge_client, deletable_club):
    """Admin (non-owner) should not be able to delete a club"""
    admin_user = User.objects.create_user(username="admin_user", display_name="Admin User")
    ClubMembership.objects.create(
        user=admin_user,
        club=deletable_club,
        role="admin"
    )
    
    bridge_client.force_login(admin_user)
    response = bridge_client.post(
        f'/groups/{deletable_club.id}/settings/delete/',
        {'level_action': 'delete'}
    )
    
    # Should be forbidden or redirected (permission denied by django-rules)
    assert response.status_code in [200, 403]
    
    # Club should NOT be deleted
    assert Club.objects.filter(id=deletable_club.id).exists()


@pytest.mark.django_db
def test_non_member_cannot_delete_club(bridge_client, user_with_no_clubs, deletable_club):
    """Non-members should not be able to delete a club"""
    bridge_client.force_login(user_with_no_clubs)
    response = bridge_client.post(
        f'/groups/{deletable_club.id}/settings/delete/',
        {'level_action': 'delete'}
    )
    
    # Should be forbidden or redirected (permission denied by django-rules)
    assert response.status_code in [200, 403]
    
    # Club should NOT be deleted
    assert Club.objects.filter(id=deletable_club.id).exists()


@pytest.mark.django_db
def test_superuser_can_delete_any_club(bridge_client, deletable_club):
    """Superusers should be able to delete any club"""
    superuser = User.objects.create_superuser(
        username="superuser",
        password="testpass",
        display_name="Super User"
    )
    
    bridge_client.force_login(superuser)
    response = bridge_client.post(
        f'/groups/{deletable_club.id}/settings/delete/',
        {'level_action': 'delete'}
    )
    
    assert response.status_code == 200
    body = response.json()
    assert body['action'] == 'redirect'
    
    # Club should be deleted
    assert not Club.objects.filter(id=deletable_club.id).exists()


# Edge case tests


@pytest.mark.django_db
def test_delete_club_without_levels(bridge_client, club_owner, deletable_club):
    """Deleting a club with no levels should work with delete option"""
    bridge_client.force_login(club_owner)
    
    response = bridge_client.post(
        f'/groups/{deletable_club.id}/settings/delete/',
        {'level_action': 'delete'}
    )
    
    assert response.status_code == 200
    assert not Club.objects.filter(id=deletable_club.id).exists()


@pytest.mark.django_db
def test_disassociate_club_without_levels(bridge_client, club_owner, deletable_club, steward_club):
    """Disassociating a club with no levels should work"""
    bridge_client.force_login(club_owner)
    
    response = bridge_client.post(
        f'/groups/{deletable_club.id}/settings/delete/',
        {'level_action': 'disassociate'}
    )
    
    assert response.status_code == 200
    assert not Club.objects.filter(id=deletable_club.id).exists()


@pytest.mark.django_db
def test_cannot_delete_nonexistent_club(bridge_client, club_owner):
    """Attempting to delete a nonexistent club should return 404"""
    bridge_client.force_login(club_owner)
    
    response = bridge_client.post(
        '/groups/nonexistent/settings/delete/',
        {'level_action': 'delete'}
    )
    
    assert response.status_code == 404


@pytest.mark.django_db
def test_disassociate_preserves_level_data(bridge_client, club_owner, club_with_levels, steward_club):
    """Disassociating should preserve all level data except club reference"""
    bridge_client.force_login(club_owner)
    
    # Get a level before deletion
    level = RDLevel.objects.filter(club=club_with_levels).first()
    original_artist = level.artist
    original_song = level.song
    original_submitter_id = level.submitter_id
    level_id = level.id
    
    response = bridge_client.post(
        f'/groups/{club_with_levels.id}/settings/delete/',
        {'level_action': 'disassociate'}
    )
    
    assert response.status_code == 200
    
    # Verify level data is preserved
    level = RDLevel.objects.get(id=level_id)
    assert level.artist == original_artist
    assert level.song == original_song
    assert level.submitter_id == original_submitter_id
    assert level.club_id == STEWARD_CLUB_ID
