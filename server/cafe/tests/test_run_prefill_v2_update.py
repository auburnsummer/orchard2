"""
Tests for the update branch of cafe.tasks.run_prefill.run_prefill_v2 (the Discord v2 add flow).

When a user updates a level with an rdzip whose sha1 already exists in the database:
- if the duplicate is a *different* level, the update is rejected (ERROR_DUPLICATE)
- if the duplicate is the *same* level (i.e. they re-uploaded the identical file), we pretend
  the update succeeded — it's a no-op — except that an NR'ed level is *not* bumped back to pending.
"""

import uuid
from unittest.mock import MagicMock, patch

import pytest
from cafe.models.add_session import AddSession, AddSessionPhase
from cafe.models.clubs.club_membership import ClubMembership
from cafe.models.rdlevels.prefill import RDLevelPrefillResult
from cafe.models.rdlevels.rdlevel import RDLevel
from cafe.models.user import User
from cafe.tasks.run_prefill import run_prefill_v2
from django.utils import timezone


@pytest.fixture
def submitter(test_club):
    user = User.objects.create_user(username="prefill_submitter", display_name="Prefill Submitter")
    ClubMembership.objects.create(user=user, club=test_club, role="admin")
    return user


def _make_level(submitter, club, sha1, approval=0, description="Old Description"):
    with patch("cafe.models.rdlevels.rdlevel.sync_level_to_typesense"):
        return RDLevel.objects.create(
            artist="Test Artist",
            artist_tokens=["test", "artist"],
            artist_raw="Test Artist",
            song="Test Song",
            song_alt="",
            song_raw="Test Song",
            seizure_warning=False,
            description=description,
            hue=90.0,
            authors=["Test Author"],
            authors_raw="Test Author",
            max_bpm=100,
            min_bpm=50,
            difficulty=1,
            single_player=True,
            two_player=False,
            last_updated=timezone.now(),
            tags=["old"],
            sha1=sha1,
            rdlevel_sha1=f"rdsha1_{uuid.uuid4().hex}",
            rd_md5=f"md5_{uuid.uuid4().hex}",
            is_animated=False,
            rdzip_url="https://old.example.com/test.rdzip",
            image_url="https://old.example.com/test.png",
            thumb_url="https://old.example.com/test.webp",
            icon_url="https://old.example.com/test_icon.png",
            submitter=submitter,
            club=club,
            approval=approval,
        )


def _make_prefill(user, club, level, sha1):
    return RDLevelPrefillResult.objects.create(
        url="https://example.com/updated.rdzip",
        version=1,
        prefill_type="update",
        user=user,
        club=club,
        level=level,
        ready=True,
        data={
            "sha1": sha1,
            "rdzip_url": "https://cdn.example.com/updated.rdzip",
            "image_url": "https://cdn.example.com/updated.png",
            "thumb_url": "https://cdn.example.com/updated.webp",
            "icon_url": "https://cdn.example.com/updated_icon.png",
        },
    )


def _make_session(user, prefill):
    return AddSession.objects.create(
        id=f"session_{uuid.uuid4().hex[:12]}",
        user=user,
        interaction_token="test_token",
        phase=AddSessionPhase.UPLOADING,
        attachments=[{"id": "att1", "filename": "level.rdzip", "url": "https://example.com/level.rdzip"}],
        selected_attachment_url="https://example.com/level.rdzip",
        add_type="update",
        prefill=prefill,
    )


@pytest.fixture
def run_task():
    """Run run_prefill_v2 locally, with the file-processing task and Discord webhook stubbed out."""
    def _run(prefill, session):
        with (
            patch("cafe.tasks.run_prefill.run_prefill", MagicMock()),
            patch("cafe.tasks.run_prefill.httpx.Client"),
            patch("cafe.models.rdlevels.rdlevel.sync_level_to_typesense"),
        ):
            run_prefill_v2.call_local(prefill.id, session.id)
        prefill.refresh_from_db()
        session.refresh_from_db()
    return _run


@pytest.mark.django_db
def test_update_with_identical_file_reports_success(submitter, test_club, run_task):
    """Re-uploading the exact same file to the same level is treated as a successful no-op update."""
    level = _make_level(submitter, test_club, sha1="same_sha1")
    prefill = _make_prefill(submitter, test_club, level, sha1="same_sha1")
    session = _make_session(submitter, prefill)

    run_task(prefill, session)

    assert session.phase == AddSessionPhase.COMPLETE
    assert session.prefill == prefill
    # the level the user selected is still the level attached to the prefill
    assert prefill.level == level

    level.refresh_from_db()
    assert level.rdzip_url == "https://cdn.example.com/updated.rdzip"
    assert level.image_url == "https://cdn.example.com/updated.png"
    assert level.thumb_url == "https://cdn.example.com/updated.webp"
    assert level.icon_url == "https://cdn.example.com/updated_icon.png"


@pytest.mark.django_db
def test_update_with_identical_file_does_not_bump_nr_level_to_pending(submitter, test_club, run_task):
    """An NR'ed level stays NR'ed when re-uploaded with the identical file (no review spamming)."""
    level = _make_level(submitter, test_club, sha1="same_sha1", approval=-1)
    prefill = _make_prefill(submitter, test_club, level, sha1="same_sha1")
    session = _make_session(submitter, prefill)

    run_task(prefill, session)

    assert session.phase == AddSessionPhase.COMPLETE
    level.refresh_from_db()
    assert level.approval == -1


@pytest.mark.django_db
def test_update_with_new_file_bumps_nr_level_to_pending(submitter, test_club, run_task):
    """A genuinely new file on an NR'ed level still re-requests review."""
    level = _make_level(submitter, test_club, sha1="old_sha1", approval=-1)
    prefill = _make_prefill(submitter, test_club, level, sha1="brand_new_sha1")
    session = _make_session(submitter, prefill)

    run_task(prefill, session)

    assert session.phase == AddSessionPhase.COMPLETE
    level.refresh_from_db()
    assert level.approval == 0
    assert level.sha1 == "brand_new_sha1"


@pytest.mark.django_db
def test_update_with_file_belonging_to_another_level_is_rejected(submitter, test_club, run_task):
    """A duplicate that is a *different* level is still an error, and the update is not applied."""
    level = _make_level(submitter, test_club, sha1="old_sha1")
    other_level = _make_level(submitter, test_club, sha1="duplicate_sha1", description="Other Description")
    prefill = _make_prefill(submitter, test_club, level, sha1="duplicate_sha1")
    session = _make_session(submitter, prefill)

    run_task(prefill, session)

    assert session.phase == AddSessionPhase.ERROR_DUPLICATE
    # the prefill is repointed at the duplicate so the Discord message can link to it
    assert prefill.level == other_level

    level.refresh_from_db()
    assert level.sha1 == "old_sha1"
    assert level.rdzip_url == "https://old.example.com/test.rdzip"
