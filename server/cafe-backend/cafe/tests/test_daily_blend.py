import datetime
import json
import pytest
from django.test import Client
from freezegun import freeze_time
from unittest.mock import patch
from cafe.models.rdlevels.daily_blend import BLEND_CUTOFF_HOUR

_TEST_DATE = "2025-12-18"
_AFTER_CUTOFF_TIME = f"{_TEST_DATE} {BLEND_CUTOFF_HOUR + 2:02d}:00:00"  # 2 hours after cutoff
_BEFORE_CUTOFF_TIME = f"{_TEST_DATE} {BLEND_CUTOFF_HOUR - 1:02d}:59:00"  # 1 minute before cutoff hour
_AT_CUTOFF_TIME = f"{_TEST_DATE} {BLEND_CUTOFF_HOUR:02d}:00:00"  # Exactly at cutoff
_BEFORE_CUTOFF_EARLY_TIME = f"{_TEST_DATE} {BLEND_CUTOFF_HOUR - 1:02d}:30:00"  # 30 min before cutoff hour


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
@freeze_time(_AFTER_CUTOFF_TIME, tz_offset=0)  # After cutoff hour GMT
def test_get_todays_blend_returns_todays_level(rdlevel):
    """Test that get_todays_blend returns the level for today after cutoff hour GMT"""
    from cafe.models.rdlevels.daily_blend import DailyBlend, get_todays_blend
    
    DailyBlend.objects.create(
        level=rdlevel,
        featured_date=datetime.date(2025, 12, 18)
    )
    
    result = get_todays_blend()
    assert result == rdlevel


@pytest.mark.django_db
@freeze_time(_AFTER_CUTOFF_TIME, tz_offset=0)  # After cutoff hour GMT
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
@freeze_time(_AFTER_CUTOFF_TIME, tz_offset=0)  # After cutoff hour GMT
def test_get_todays_blend_returns_none_if_no_blends():
    """Test that get_todays_blend returns None if there are no blends at all"""
    from cafe.models.rdlevels.daily_blend import get_todays_blend
    
    result = get_todays_blend()
    assert result is None


@pytest.mark.django_db
@freeze_time(_AFTER_CUTOFF_TIME, tz_offset=0)  # After cutoff hour GMT
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
@freeze_time(_BEFORE_CUTOFF_TIME, tz_offset=0)  # Before cutoff hour GMT
def test_get_todays_blend_before_cutoff_returns_yesterday(rdlevel, second_rdlevel):
    """Test that get_todays_blend returns yesterday's blend before cutoff hour GMT"""
    from cafe.models.rdlevels.daily_blend import DailyBlend, get_todays_blend
    
    # Create blend for today (Dec 18) - should NOT be returned before cutoff
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
@freeze_time(_AT_CUTOFF_TIME, tz_offset=0)  # Exactly at cutoff hour GMT
def test_get_todays_blend_at_cutoff_returns_today(rdlevel, second_rdlevel):
    """Test that get_todays_blend returns today's blend at exactly cutoff hour GMT"""
    from cafe.models.rdlevels.daily_blend import DailyBlend, get_todays_blend
    
    # Create blend for today (Dec 18) - should be returned at/after cutoff
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
@freeze_time(_BEFORE_CUTOFF_EARLY_TIME, tz_offset=0)  # Before cutoff hour GMT
def test_get_todays_blend_before_cutoff_falls_back_to_past(rdlevel):
    """Test that before cutoff hour GMT, if no yesterday blend, falls back to most recent past"""
    from cafe.models.rdlevels.daily_blend import DailyBlend, get_todays_blend
    
    # Create blend for today only - should not be returned before cutoff
    DailyBlend.objects.create(
        level=rdlevel,
        featured_date=datetime.date(2025, 12, 18)
    )
    
    result = get_todays_blend()
    # Before cutoff on Dec 18, blend_date is Dec 17, and there's no blend for Dec 17
    # So it falls back to the most recent past blend before Dec 17, which is None
    assert result is None


# ============== Fixtures ==============

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
