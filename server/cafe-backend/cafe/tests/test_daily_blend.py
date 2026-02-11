import datetime
import json
import pytest
from django.test import Client
from freezegun import freeze_time
from unittest.mock import patch


@pytest.mark.django_db
def test_daily_blend_unique_date_constraint(rdlevel, second_rdlevel):
    """Test that only one level can be blended per day"""
    from cafe.models.rdlevels.daily_blend import DailyBlend
    from django.db import IntegrityError
    
    DailyBlend.objects.create(
        level=rdlevel,
        featured_date=datetime.date(2025, 12, 18)
    )
    
    with pytest.raises(IntegrityError):
        DailyBlend.objects.create(
            level=second_rdlevel,
            featured_date=datetime.date(2025, 12, 18)
        )

@pytest.mark.django_db
@freeze_time("2025-12-18 06:00:00", tz_offset=0)  # After 5:00 AM GMT
def test_get_todays_blend_returns_todays_level(rdlevel):
    """Test that get_todays_blend returns the level for today after 5:00 AM GMT"""
    from cafe.models.rdlevels.daily_blend import DailyBlend, get_todays_blend
    
    DailyBlend.objects.create(
        level=rdlevel,
        featured_date=datetime.date(2025, 12, 18)
    )
    
    result = get_todays_blend()
    assert result == rdlevel


@pytest.mark.django_db
@freeze_time("2025-12-18 06:00:00", tz_offset=0)  # After 5:00 AM GMT
def test_get_todays_blend_returns_most_recent_past_if_no_today(rdlevel, second_rdlevel):
    """Test that get_todays_blend returns the most recent past blend if no blend for today"""
    from cafe.models.rdlevels.daily_blend import DailyBlend, get_todays_blend
    
    # Create blends for past dates, but not today
    DailyBlend.objects.create(
        level=rdlevel,
        featured_date=datetime.date(2025, 12, 15)
    )
    DailyBlend.objects.create(
        level=second_rdlevel,
        featured_date=datetime.date(2025, 12, 17)
    )
    
    result = get_todays_blend()
    assert result == second_rdlevel  # Most recent past blend


@pytest.mark.django_db
@freeze_time("2025-12-18 06:00:00", tz_offset=0)  # After 5:00 AM GMT
def test_get_todays_blend_returns_none_if_no_blends():
    """Test that get_todays_blend returns None if there are no blends at all"""
    from cafe.models.rdlevels.daily_blend import get_todays_blend
    
    result = get_todays_blend()
    assert result is None


@pytest.mark.django_db
@freeze_time("2025-12-18 06:00:00", tz_offset=0)  # After 5:00 AM GMT
def test_get_todays_blend_ignores_future_blends(rdlevel, second_rdlevel):
    """Test that get_todays_blend ignores future blends when falling back"""
    from cafe.models.rdlevels.daily_blend import DailyBlend, get_todays_blend
    
    # Create a blend for the future only
    DailyBlend.objects.create(
        level=rdlevel,
        featured_date=datetime.date(2025, 12, 20)
    )
    # Create a blend for the past
    DailyBlend.objects.create(
        level=second_rdlevel,
        featured_date=datetime.date(2025, 12, 15)
    )
    
    result = get_todays_blend()
    assert result == second_rdlevel  # Should return past blend, not future


@pytest.mark.django_db
@freeze_time("2025-12-18 04:59:00", tz_offset=0)  # Before 5:00 AM GMT
def test_get_todays_blend_before_cutoff_returns_yesterday(rdlevel, second_rdlevel):
    """Test that get_todays_blend returns yesterday's blend before 5:00 AM GMT cutoff"""
    from cafe.models.rdlevels.daily_blend import DailyBlend, get_todays_blend
    
    # Create blend for today (Dec 18) - should NOT be returned before 5:00 AM
    DailyBlend.objects.create(
        level=rdlevel,
        featured_date=datetime.date(2025, 12, 18)
    )
    # Create blend for yesterday (Dec 17) - should be returned
    DailyBlend.objects.create(
        level=second_rdlevel,
        featured_date=datetime.date(2025, 12, 17)
    )
    
    result = get_todays_blend()
    assert result == second_rdlevel  # Should return yesterday's blend


@pytest.mark.django_db
@freeze_time("2025-12-18 05:00:00", tz_offset=0)  # Exactly 5:00 AM GMT
def test_get_todays_blend_at_cutoff_returns_today(rdlevel, second_rdlevel):
    """Test that get_todays_blend returns today's blend at exactly 5:00 AM GMT"""
    from cafe.models.rdlevels.daily_blend import DailyBlend, get_todays_blend
    
    # Create blend for today (Dec 18) - should be returned at/after 5:00 AM
    DailyBlend.objects.create(
        level=rdlevel,
        featured_date=datetime.date(2025, 12, 18)
    )
    # Create blend for yesterday (Dec 17)
    DailyBlend.objects.create(
        level=second_rdlevel,
        featured_date=datetime.date(2025, 12, 17)
    )
    
    result = get_todays_blend()
    assert result == rdlevel  # Should return today's blend


@pytest.mark.django_db
@freeze_time("2025-12-18 04:30:00", tz_offset=0)  # Before 5:00 AM GMT
def test_get_todays_blend_before_cutoff_falls_back_to_past(rdlevel):
    """Test that before 5:00 AM GMT, if no yesterday blend, falls back to most recent past"""
    from cafe.models.rdlevels.daily_blend import DailyBlend, get_todays_blend
    
    # Create blend for today only - should not be returned before cutoff
    DailyBlend.objects.create(
        level=rdlevel,
        featured_date=datetime.date(2025, 12, 18)
    )
    
    result = get_todays_blend()
    # Before 5 AM on Dec 18, blend_date is Dec 17, and there's no blend for Dec 17
    # So it falls back to the most recent past blend before Dec 17, which is None
    assert result is None



@pytest.mark.django_db
def test_set_daily_blend_requires_at_least_one_identifier(client: Client, pharmacist_user):
    """Test that set_daily_blend requires either level_id or level_url"""
    client.force_login(pharmacist_user)
    
    response = client.post(
        '/api/set_daily_blend/',
        data=json.dumps({'featured_date': None}),
        content_type='application/json'
    )
    assert response.status_code == 400
    assert response.json()['error'] == 'Either level_id or level_url must be provided'


@pytest.mark.django_db
def test_set_daily_blend_requires_permission(client: Client, rdlevel, user_with_no_clubs):
    """Test that set_daily_blend requires blend permission"""
    client.force_login(user_with_no_clubs)
    
    response = client.post(
        '/api/set_daily_blend/',
        data=json.dumps({'level_id': rdlevel.id, 'featured_date': None}),
        content_type='application/json'
    )
    assert response.status_code == 403
    assert response.json()['error'] == 'Permission denied'


@pytest.mark.django_db
def test_set_daily_blend_requires_permission_with_level_url(client: Client, rdlevel, user_with_no_clubs):
    """Test that set_daily_blend requires blend permission when using level_url"""
    client.force_login(user_with_no_clubs)
    
    response = client.post(
        '/api/set_daily_blend/',
        data=json.dumps({'level_url': rdlevel.rdzip_url, 'featured_date': None}),
        content_type='application/json'
    )
    assert response.status_code == 403
    assert response.json()['error'] == 'Permission denied'


@pytest.mark.django_db
def test_set_daily_blend_returns_404_for_nonexistent_level(client: Client, pharmacist_user):
    """Test that set_daily_blend returns 404 for nonexistent level"""
    client.force_login(pharmacist_user)
    
    response = client.post(
        '/api/set_daily_blend/',
        data=json.dumps({'level_id': 'nonexistent_id', 'featured_date': None}),
        content_type='application/json'
    )
    assert response.status_code == 404


@pytest.mark.django_db
def test_set_daily_blend_returns_404_for_nonexistent_level_url(client: Client, pharmacist_user):
    """Test that set_daily_blend returns 404 for nonexistent level_url"""
    client.force_login(pharmacist_user)
    
    response = client.post(
        '/api/set_daily_blend/',
        data=json.dumps({'level_url': 'https://example.com/nonexistent.rdzip', 'featured_date': None}),
        content_type='application/json'
    )
    assert response.status_code == 404


@pytest.mark.django_db
@freeze_time("2025-12-18")
def test_set_daily_blend_sets_today_when_no_date_provided(client: Client, rdlevel, pharmacist_user):
    """Test that set_daily_blend sets today's date when featured_date is None"""
    from cafe.models.rdlevels.daily_blend import DailyBlend
    
    client.force_login(pharmacist_user)
    
    response = client.post(
        '/api/set_daily_blend/',
        data=json.dumps({'level_id': rdlevel.id, 'featured_date': None}),
        content_type='application/json'
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['featured_date'] == '2025-12-18'
    assert data['level']['id'] == rdlevel.id
    
    # Verify in database
    blend = DailyBlend.objects.get(featured_date=datetime.date(2025, 12, 18))
    assert blend.level == rdlevel


@pytest.mark.django_db
@freeze_time("2025-12-18")
def test_set_daily_blend_with_specific_future_date(client: Client, rdlevel, pharmacist_user):
    """Test that set_daily_blend can set a specific future date"""
    from cafe.models.rdlevels.daily_blend import DailyBlend
    
    client.force_login(pharmacist_user)
    
    response = client.post(
        '/api/set_daily_blend/',
        data=json.dumps({'level_id': rdlevel.id, 'featured_date': '2025-12-25'}),
        content_type='application/json'
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['featured_date'] == '2025-12-25'
    
    # Verify in database
    blend = DailyBlend.objects.get(featured_date=datetime.date(2025, 12, 25))
    assert blend.level == rdlevel


@pytest.mark.django_db
@freeze_time("2025-12-18")
def test_set_daily_blend_with_level_url(client: Client, rdlevel, pharmacist_user):
    """Test that set_daily_blend works with level_url parameter"""
    from cafe.models.rdlevels.daily_blend import DailyBlend
    
    client.force_login(pharmacist_user)
    
    response = client.post(
        '/api/set_daily_blend/',
        data=json.dumps({'level_url': rdlevel.rdzip_url, 'featured_date': None}),
        content_type='application/json'
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['featured_date'] == '2025-12-18'
    assert data['level']['id'] == rdlevel.id
    
    # Verify in database
    blend = DailyBlend.objects.get(featured_date=datetime.date(2025, 12, 18))
    assert blend.level == rdlevel


@pytest.mark.django_db
@freeze_time("2025-12-18")
def test_set_daily_blend_rejects_past_date(client: Client, rdlevel, pharmacist_user):
    """Test that set_daily_blend rejects past dates"""
    client.force_login(pharmacist_user)
    
    response = client.post(
        '/api/set_daily_blend/',
        data=json.dumps({'level_id': rdlevel.id, 'featured_date': '2025-12-17'}),
        content_type='application/json'
    )
    
    assert response.status_code == 400
    assert response.json()['error'] == 'Cannot set daily blend for past dates'


@pytest.mark.django_db
@freeze_time("2025-12-18")
def test_set_daily_blend_updates_existing_blend(client: Client, rdlevel, second_rdlevel, pharmacist_user):
    """Test that set_daily_blend updates an existing blend for the same date"""
    from cafe.models.rdlevels.daily_blend import DailyBlend
    
    # Create an existing blend for today
    DailyBlend.objects.create(
        level=rdlevel,
        featured_date=datetime.date(2025, 12, 18)
    )
    
    client.force_login(pharmacist_user)
    
    response = client.post(
        '/api/set_daily_blend/',
        data=json.dumps({'level_id': second_rdlevel.id, 'featured_date': '2025-12-18'}),
        content_type='application/json'
    )
    
    assert response.status_code == 200
    
    # Verify only one blend exists for today and it's the new one
    blends = DailyBlend.objects.filter(featured_date=datetime.date(2025, 12, 18))
    assert blends.count() == 1
    assert blends.first().level == second_rdlevel


# ============== Fixtures ==============

@pytest.fixture
def pharmacy_club():
    """Create the pharmacy club (cpharmacy)"""
    from cafe.models.clubs.club import Club
    from orchard.settings import PHARMACY_CLUB_ID
    return Club.objects.create(id=PHARMACY_CLUB_ID, name="Pharmacy")


@pytest.fixture
def pharmacist_user(pharmacy_club):
    """Create a user who is an admin of the pharmacy club (a pharmacist)"""
    from cafe.models.user import User
    from cafe.models.clubs.club_membership import ClubMembership
    
    user = User.objects.create_user(username="pharmacist_user", display_name="Pharmacist User")
    ClubMembership.objects.create(
        user=user,
        club=pharmacy_club,
        role="admin"
    )
    return user


@pytest.fixture
def second_rdlevel(test_club):
    """Create a second test RDLevel for testing"""
    from cafe.models.rdlevels.rdlevel import RDLevel
    from cafe.models.user import User
    from django.utils import timezone
    from unittest.mock import patch
    
    submitter = User.objects.create_user(username="test_submitter_2", display_name="Test Submitter 2")
    
    with patch('cafe.models.rdlevels.rdlevel.sync_level_to_typesense'):
        return RDLevel.objects.create(
            artist="Second Artist",
            artist_tokens=["second", "artist"],
            artist_raw="Second Artist",
            song="Second Song",
            song_alt="Second Song Alt",
            song_raw="Second Song",
            seizure_warning=False,
            description="A second test level",
            hue=90.0,
            authors=["Second Author"],
            authors_raw="Second Author",
            max_bpm=140,
            min_bpm=70,
            difficulty=2,
            single_player=True,
            two_player=False,
            last_updated=timezone.now(),
            tags=["test", "second"],
            sha1="second_sha1_hash_12345",
            rdlevel_sha1="second_rdlevel_sha1_hash_12345",
            rd_md5="second_md5_hash_12345",
            is_animated=False,
            rdzip_url="https://example.com/second.rdzip",
            image_url="https://example.com/second_image.jpg",
            thumb_url="https://example.com/second_thumb.jpg",
            icon_url="https://example.com/second_icon.jpg",
            submitter=submitter,
            club=test_club,
            approval=0
        )
