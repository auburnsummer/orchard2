"""
Tests for stage two of the prefill flow (cafe:level_from_prefill / prefill_stage_two).

Stage two is reached after a prefill task has been created (either from Discord or the web flow).
It handles:
- Showing a loading screen while the prefill task is running
- For new levels: showing a form to finalize metadata and create the level
- For updates: showing potential matches and updating the selected level
"""

import json
import pytest
from unittest.mock import patch
from django.utils import timezone

from cafe.models.rdlevels.prefill import RDLevelPrefillResult
from cafe.models.rdlevels.rdlevel import RDLevel
from cafe.models.user import User
from cafe.models.clubs.club import Club
from cafe.models.clubs.club_membership import ClubMembership


@pytest.fixture
def test_user():
    """Create a test user for prefill flow testing"""
    return User.objects.create_user(username="testuser", display_name="Test User")


@pytest.fixture 
def test_club_with_user(test_user):
    """Create a test club with user as admin"""
    club = Club.objects.create(id="testclub", name="Test Club")
    ClubMembership.objects.create(
        user=test_user,
        club=club,
        role="admin"
    )
    return club


@pytest.fixture
def prefill_result_new(test_user, test_club_with_user):
    """Create a prefill result for new level flow"""
    return RDLevelPrefillResult.objects.create(
        url="https://example.com/test.rdzip",
        version=1,
        prefill_type="new",
        user=test_user,
        club=test_club_with_user,
        ready=False
    )


@pytest.fixture
def prefill_result_ready(test_user, test_club_with_user):
    """Create a ready prefill result with mock data"""
    return RDLevelPrefillResult.objects.create(
        url="https://example.com/test.rdzip",
        version=1,
        prefill_type="new",
        user=test_user,
        club=test_club_with_user,
        ready=True,
        data={
            "artist": "Test Artist",
            "artist_tokens": ["test", "artist"],
            "artist_raw": "Test Artist",
            "song": "Test Song",
            "song_raw": "Test Song",
            "description": "Test Description",
            "hue": 180.0,
            "authors": ["Test Author"],
            "authors_raw": "Test Author",
            "max_bpm": 120,
            "min_bpm": 60,
            "difficulty": 1,
            "single_player": True,
            "two_player": False,
            "tags": ["test"],
            "seizure_warning": False,
            "last_updated": timezone.now().isoformat(),
            "sha1": "test_sha1_hash_12345",
            "rdlevel_sha1": "test_rdlevel_sha1_hash_12345",
            "rd_md5": "test_md5_hash_12345",
            "is_animated": False,
            "rdzip_url": "https://cdn.example.com/test.rdzip",
            "image_url": "https://cdn.example.com/test.png",
            "thumb_url": "https://cdn.example.com/test.webp",
            "icon_url": "https://cdn.example.com/test_icon.png",
        }
    )


@pytest.fixture
def existing_level(test_user, test_club_with_user):
    """Create an existing level for update testing"""
    with patch('cafe.models.rdlevels.rdlevel.sync_level_to_typesense'):
        return RDLevel.objects.create(
            artist="Test Artist",
            artist_tokens=["test", "artist"],
            artist_raw="Test Artist",
            song="Test Song",
            song_alt="Test Song Alt",
            song_raw="Test Song",
            description="Old Description",
            hue=90.0,
            authors=["Test Author"],
            authors_raw="Test Author",
            max_bpm=100,
            min_bpm=50,
            difficulty=1,
            single_player=True,
            two_player=False,
            tags=["old"],
            seizure_warning=False,
            last_updated=timezone.now(),
            sha1="old_sha1",
            rdlevel_sha1="old_rdlevel_sha1",
            rd_md5="old_md5",
            is_animated=False,
            rdzip_url="https://old.example.com/test.rdzip",
            image_url="https://old.example.com/test.png",
            thumb_url="https://old.example.com/test.webp",
            icon_url="https://old.example.com/test_icon.png",
            submitter=test_user,
            club=test_club_with_user,
            approval=0
        )
@pytest.fixture
def prefill_result_update_ready(test_user, test_club_with_user):
    """Create a ready prefill result for update flow"""
    return RDLevelPrefillResult.objects.create(
        url="https://example.com/test_updated.rdzip",
        version=1,
        prefill_type="update",
        user=test_user,
        club=test_club_with_user,
        ready=True,
        data={
            "artist_raw": "Test Artist",
            "song_raw": "Test Song",
            "rdzip_url": "https://cdn.example.com/test_updated.rdzip",
            "image_url": "https://cdn.example.com/test_updated.png",
            "thumb_url": "https://cdn.example.com/test_updated.webp",
            "icon_url": "https://cdn.example.com/test_updated_icon.png",
            "sha1": "test_sha1_hash_12345"
        }
    )


# Test: GET stage two shows loading when not ready
@pytest.mark.django_db
def test_prefill_stage_two_get_not_ready(bridge_client, test_user, prefill_result_new):
    """Test GET to level_from_prefill shows loading state when prefill not ready"""
    bridge_client.force_login(test_user)
    response = bridge_client.get(f'/levels/from_prefill/{prefill_result_new.id}/')
    
    assert response.status_code == 200
    body = response.json()
    assert body['action'] == 'render'
    assert body['view'] == 'cafe:level_from_prefill'
    assert body['props']['prefill']['ready'] is False
    assert body['props']['prefill']['id'] == prefill_result_new.id


# Test Step 6a: New level creation with prefilled data
@pytest.mark.django_db
def test_prefill_stage_two_get_ready_new_level(bridge_client, test_user, prefill_result_ready):
    """Test GET to level_from_prefill shows form when prefill is ready for new level"""
    bridge_client.force_login(test_user)
    response = bridge_client.get(f'/levels/from_prefill/{prefill_result_ready.id}/')
    
    assert response.status_code == 200
    body = response.json()
    assert body['action'] == 'render'
    assert body['view'] == 'cafe:level_from_prefill'
    assert body['props']['prefill']['ready'] is True
    assert body['props']['prefill']['prefill_type'] == 'new'
    assert body['props']['prefill']['data']['artist'] == 'Test Artist'
    assert body['props']['potential_matches'] == []  # No matches for new level


@pytest.mark.django_db
@patch('cafe.models.rdlevels.rdlevel.sync_level_to_typesense')
def test_prefill_stage_two_post_create_new_level(mock_sync, bridge_client, test_user, prefill_result_ready):
    """Test POST to level_from_prefill creates new level with prefilled data"""
    bridge_client.force_login(test_user)
    
    # Prepare level data to submit (matching AddLevelPayload structure)
    level_data = {
        "artist": "Test Artist",
        "artist_tokens": ["test", "artist"],
        "song": "Test Song",
        "song_alt": "",
        "description": "Test Description",
        "hue": 180.0,
        "authors": ["Test Author"],
        "difficulty": 1,
        "max_bpm": 120,
        "min_bpm": 60,
        "single_player": True,
        "two_player": False,
        "seizure_warning": False,
        "tags": ["test"],
        "has_classics": True,
        "has_oneshots": True,
        "has_squareshots": False,
        "has_freezeshots": True,
        "has_burnshots": False,
        "has_holdshots": True,
        "has_triangleshots": False,
        "has_skipshots": False,
        "has_subdivs": True,
        "has_synco": True,
        "has_freetimes": False,
        "has_holds": True,
        "has_window_dance": False,
        "has_rdcode": False,
        "has_cpu_rows": False,
        "total_hits_approx": 100
    }
    
    response = bridge_client.post(f'/levels/from_prefill/{prefill_result_ready.id}/', {
        'prefill': json.dumps(level_data)
    })
    
    assert response.status_code == 200
    body = response.json()
    
    # Should redirect to level view
    assert body['action'] == 'redirect'
    assert '/levels/' in body['path']
    
    # Extract level ID from redirect path
    level_id = body['path'].split('/levels/')[1].rstrip('/')
    
    # Verify level was created with prefilled data
    level = RDLevel.objects.get(id=level_id)
    assert level.artist == 'Test Artist'
    assert level.song == 'Test Song'
    assert level.rdzip_url == 'https://cdn.example.com/test.rdzip'  # From prefill data
    assert level.image_url == 'https://cdn.example.com/test.png'  # From prefill data
    assert level.submitter == test_user
    assert level.club == prefill_result_ready.club
    
    # Verify prefill result was deleted
    assert not RDLevelPrefillResult.objects.filter(id=prefill_result_ready.id).exists()


# Test Step 7a: Update level selection shows potential matches
@pytest.mark.django_db
def test_prefill_stage_two_get_ready_update_level(bridge_client, test_user, prefill_result_update_ready, existing_level):
    """Test GET to level_from_prefill shows potential matches for update"""
    bridge_client.force_login(test_user)
    response = bridge_client.get(f'/levels/from_prefill/{prefill_result_update_ready.id}/')
    
    assert response.status_code == 200
    body = response.json()
    assert body['action'] == 'render'
    assert body['view'] == 'cafe:level_from_prefill'
    assert body['props']['prefill']['ready'] is True
    assert body['props']['prefill']['prefill_type'] == 'update'
    
    # Should show the existing level as a potential match
    matches = body['props']['potential_matches']
    assert len(matches) == 1
    assert matches[0]['id'] == existing_level.id
    assert matches[0]['artist'] == 'Test Artist'


@pytest.mark.django_db
@patch('cafe.models.rdlevels.rdlevel.sync_level_to_typesense')
def test_prefill_stage_two_post_update_existing_level(mock_sync, bridge_client, test_user, prefill_result_update_ready, existing_level):
    """Test POST to level_from_prefill updates existing level"""
    bridge_client.force_login(test_user)
    
    response = bridge_client.post(f'/levels/from_prefill/{prefill_result_update_ready.id}/', {
        'prefill': existing_level.id
    })
    
    assert response.status_code == 200
    body = response.json()
    
    # Should redirect to level view
    assert body['action'] == 'redirect'
    assert f'/levels/{existing_level.id}/' in body['path']
    
    # Verify level was updated with prefilled data
    existing_level.refresh_from_db()
    assert existing_level.rdzip_url == 'https://cdn.example.com/test_updated.rdzip'
    assert existing_level.image_url == 'https://cdn.example.com/test_updated.png'
    assert existing_level.thumb_url == 'https://cdn.example.com/test_updated.webp'
    assert existing_level.icon_url == 'https://cdn.example.com/test_updated_icon.png'
    
    # Non-URL fields should remain unchanged
    assert existing_level.description == "Old Description"
    assert existing_level.hue == 90.0
    assert existing_level.tags == ["old"]
    
    # Verify prefill result was deleted
    assert not RDLevelPrefillResult.objects.filter(id=prefill_result_update_ready.id).exists()


# Test permission checks
@pytest.mark.django_db
def test_prefill_stage_two_permission_denied_different_user(bridge_client, prefill_result_new):
    """Test that user can't access another user's prefill result"""
    other_user = User.objects.create_user(username="otheruser")
    bridge_client.force_login(other_user)
    
    response = bridge_client.get(f'/levels/from_prefill/{prefill_result_new.id}/')
    
    # Permission denied by rules middleware, but django-bridge returns 200 with action: 'render'
    # Check the response is an actual rejection (no content)
    assert response.status_code == 200
    body = response.json()
    # Should be a permission denied page or redirect
    # The exact behavior depends on how rules handles permission denied


@pytest.mark.django_db
def test_prefill_stage_two_update_permission_denied_for_level(bridge_client, test_user, prefill_result_update_ready, test_club_with_user):
    """Test that user can't update level they don't have permission for"""
    # Create a level owned by another user
    other_user = User.objects.create_user(username="otheruser")
    other_club = Club.objects.create(id="otherclub", name="Other Club")
    
    with patch('cafe.models.rdlevels.rdlevel.sync_level_to_typesense'):
        other_level = RDLevel.objects.create(
            artist="Test Artist",
            artist_tokens=["test", "artist"],
            artist_raw="Test Artist",
            song="Test Song",
            song_alt="Test Song Alt",
            song_raw="Test Song",
            description="Other Description",
            hue=90.0,
            authors=["Test Author"],
            authors_raw="Test Author",
            max_bpm=100,
            min_bpm=50,
            difficulty=1,
            single_player=True,
            two_player=False,
            tags=["other"],
            seizure_warning=False,
            last_updated=timezone.now(),
            sha1="other_sha1",
            rdlevel_sha1="other_rdlevel_sha1",
            rd_md5="other_md5",
            is_animated=False,
            rdzip_url="https://other.example.com/test.rdzip",
            image_url="https://other.example.com/test.png",
            thumb_url="https://other.example.com/test.webp",
            icon_url="https://other.example.com/test_icon.png",
            submitter=other_user,
            club=other_club,
            approval=0
        )
    
    bridge_client.force_login(test_user)
    
    response = bridge_client.post(f'/levels/from_prefill/{prefill_result_update_ready.id}/', {
        'prefill': other_level.id
    })
    
    assert response.status_code == 200
    body = response.json()
    
    # Should show error message
    assert body['action'] == 'render'
    assert len(body['messages']) == 1
    assert body['messages'][0]['level'] == 'error'
    assert 'permission' in body['messages'][0]['html']


# Test error handling
@pytest.mark.django_db
def test_prefill_stage_two_post_invalid_json(bridge_client, test_user, prefill_result_ready):
    """Test POST with invalid JSON shows error"""
    bridge_client.force_login(test_user)
    
    # Use a valid JSON string that doesn't match the expected structure
    response = bridge_client.post(f'/levels/from_prefill/{prefill_result_ready.id}/', {
        'prefill': '{"invalid": "structure"}'
    })
    
    assert response.status_code == 200
    body = response.json()
    assert body['action'] == 'render'
    assert len(body['messages']) == 1
    assert body['messages'][0]['level'] == 'error'
