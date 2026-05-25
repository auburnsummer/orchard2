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


# ============== Tests: get_todays_blend with pool-only blend ==============

@pytest.mark.django_db
@freeze_time(_AFTER_CUTOFF_TIME, tz_offset=0)
def test_get_todays_blend_falls_back_when_today_has_pool_only(rdlevel, default_blend_pool):
    """If today's DailyBlend is pool-only (not yet resolved), fall back to most recent past resolved blend"""
    from cafe.models.rdlevels.daily_blend import DailyBlend, get_todays_blend

    DailyBlend.objects.create(
        pool=default_blend_pool,
        featured_date=datetime.date(2025, 12, 18)
    )
    DailyBlend.objects.create(
        level=rdlevel,
        featured_date=datetime.date(2025, 12, 17)
    )

    result = get_todays_blend()
    assert result == rdlevel


@pytest.mark.django_db
@freeze_time(_AFTER_CUTOFF_TIME, tz_offset=0)
def test_get_todays_blend_returns_none_when_today_has_pool_only_and_no_past(default_blend_pool):
    """If today's DailyBlend is pool-only and there's no past resolved blend, return None"""
    from cafe.models.rdlevels.daily_blend import DailyBlend, get_todays_blend

    DailyBlend.objects.create(
        pool=default_blend_pool,
        featured_date=datetime.date(2025, 12, 18)
    )

    result = get_todays_blend()
    assert result is None


# ============== Tests: todays_blend_or_default ==============

@pytest.mark.django_db
@freeze_time(_AFTER_CUTOFF_TIME, tz_offset=0)
def test_todays_blend_or_default_returns_existing_level_blend(rdlevel, default_blend_pool):
    """Returns existing DailyBlend for today if it already has a level"""
    from cafe.models.rdlevels.daily_blend import DailyBlend
    from cafe.tasks.run_daily_blend import todays_blend_or_default

    existing = DailyBlend.objects.create(
        level=rdlevel,
        featured_date=datetime.date(2025, 12, 18)
    )

    result = todays_blend_or_default()
    assert result == existing
    assert DailyBlend.objects.count() == 1


@pytest.mark.django_db
@freeze_time(_AFTER_CUTOFF_TIME, tz_offset=0)
def test_todays_blend_or_default_returns_existing_pool_blend(default_blend_pool):
    """Returns existing DailyBlend for today if it already has a pool"""
    from cafe.models.rdlevels.daily_blend import DailyBlend
    from cafe.tasks.run_daily_blend import todays_blend_or_default

    existing = DailyBlend.objects.create(
        pool=default_blend_pool,
        featured_date=datetime.date(2025, 12, 18)
    )

    result = todays_blend_or_default()
    assert result == existing
    assert DailyBlend.objects.count() == 1


@pytest.mark.django_db
@freeze_time(_AFTER_CUTOFF_TIME, tz_offset=0)
def test_todays_blend_or_default_creates_default_pool_blend_when_none_today(default_blend_pool):
    """When no DailyBlend exists for today, creates one pointing to the default pool"""
    from cafe.models.rdlevels.daily_blend import DailyBlend
    from cafe.tasks.run_daily_blend import todays_blend_or_default

    result = todays_blend_or_default()

    assert DailyBlend.objects.count() == 1
    assert result.pool == default_blend_pool
    assert result.level is None
    assert result.featured_date == datetime.date(2025, 12, 18)


# ============== Tests: resolve_pool_blend ==============

@pytest.mark.django_db
def test_resolve_pool_blend_no_op_when_level_already_set(rdlevel, default_blend_pool):
    """Returns blend unchanged and does not consume pool entries when level is already set"""
    from cafe.models.rdlevels.daily_blend import DailyBlend
    from cafe.models.rdlevels.blend_random_pool import DailyBlendRandomPool
    from cafe.tasks.run_daily_blend import resolve_pool_blend

    blend = DailyBlend.objects.create(
        level=rdlevel,
        featured_date=datetime.date(2025, 12, 18)
    )
    DailyBlendRandomPool.objects.create(level=rdlevel, pool=default_blend_pool)

    resolve_pool_blend(blend)

    assert blend.level == rdlevel
    assert DailyBlendRandomPool.objects.count() == 1  # pool entry not consumed


@pytest.mark.django_db
def test_resolve_pool_blend_picks_level_from_pool(rdlevel, default_blend_pool):
    """Resolves a pool-based DailyBlend to a specific level from the pool"""
    from cafe.models.rdlevels.daily_blend import DailyBlend
    from cafe.models.rdlevels.blend_random_pool import DailyBlendRandomPool
    from cafe.tasks.run_daily_blend import resolve_pool_blend

    blend = DailyBlend.objects.create(
        pool=default_blend_pool,
        featured_date=datetime.date(2025, 12, 18)
    )
    DailyBlendRandomPool.objects.create(level=rdlevel, pool=default_blend_pool)

    resolve_pool_blend(blend)

    assert blend.level == rdlevel
    assert blend.pool is None


@pytest.mark.django_db
def test_resolve_pool_blend_persists_to_db(rdlevel, default_blend_pool):
    """After resolution, the level is saved to the database and pool is cleared"""
    from cafe.models.rdlevels.daily_blend import DailyBlend
    from cafe.models.rdlevels.blend_random_pool import DailyBlendRandomPool
    from cafe.tasks.run_daily_blend import resolve_pool_blend

    blend = DailyBlend.objects.create(
        pool=default_blend_pool,
        featured_date=datetime.date(2025, 12, 18)
    )
    DailyBlendRandomPool.objects.create(level=rdlevel, pool=default_blend_pool)

    resolve_pool_blend(blend)
    blend.refresh_from_db()

    assert blend.level == rdlevel
    assert blend.pool is None


@pytest.mark.django_db
def test_resolve_pool_blend_deletes_pool_entry(rdlevel, default_blend_pool):
    """Consumes (deletes) the chosen entry from the pool after resolving"""
    from cafe.models.rdlevels.daily_blend import DailyBlend
    from cafe.models.rdlevels.blend_random_pool import DailyBlendRandomPool
    from cafe.tasks.run_daily_blend import resolve_pool_blend

    blend = DailyBlend.objects.create(
        pool=default_blend_pool,
        featured_date=datetime.date(2025, 12, 18)
    )
    DailyBlendRandomPool.objects.create(level=rdlevel, pool=default_blend_pool)

    resolve_pool_blend(blend)

    assert DailyBlendRandomPool.objects.count() == 0


@pytest.mark.django_db
def test_resolve_pool_blend_only_picks_from_assigned_pool(rdlevel, second_rdlevel, default_blend_pool):
    """Picks only from the pool assigned to the blend, not other pools"""
    from cafe.models.rdlevels.blend_pool import BlendPool
    from cafe.models.rdlevels.daily_blend import DailyBlend
    from cafe.models.rdlevels.blend_random_pool import DailyBlendRandomPool
    from cafe.tasks.run_daily_blend import resolve_pool_blend

    other_pool = BlendPool.objects.create(name="Other Pool")
    blend = DailyBlend.objects.create(
        pool=default_blend_pool,
        featured_date=datetime.date(2025, 12, 18)
    )
    # Only put second_rdlevel in the other pool — default_blend_pool is empty
    DailyBlendRandomPool.objects.create(level=second_rdlevel, pool=other_pool)

    resolve_pool_blend(blend)

    assert blend.level is None  # default_blend_pool is empty, other pool ignored


@pytest.mark.django_db
def test_resolve_pool_blend_returns_none_when_pool_empty(default_blend_pool):
    """Returns None and leaves blend unmodified when the pool has no entries"""
    from cafe.models.rdlevels.daily_blend import DailyBlend
    from cafe.tasks.run_daily_blend import resolve_pool_blend

    blend = DailyBlend.objects.create(
        pool=default_blend_pool,
        featured_date=datetime.date(2025, 12, 18)
    )

    resolve_pool_blend(blend)

    assert blend.level is None


# ============== Fixtures ==============

@pytest.fixture
def default_blend_pool():
    """Fetch the default blend pool (created by migration)"""
    from cafe.models.rdlevels.blend_pool import BlendPool, DEFAULT_BLEND_POOL_ID
    pool, _ = BlendPool.objects.get_or_create(id=DEFAULT_BLEND_POOL_ID, defaults={"name": "Default Pool"})
    return pool


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
