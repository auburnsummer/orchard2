"""Tests that blend views call report_blend_change when configuration changes occur."""

import datetime
import pytest
from unittest.mock import patch

from django.urls import reverse


# ============== Fixtures ==============


@pytest.fixture
def pharmacy_club():
    from cafe.models.clubs.club import Club
    return Club.objects.create(id="cpharmacy", name="Pharmacy")


@pytest.fixture
def blend_user(pharmacy_club):
    from cafe.models.user import User
    from cafe.models.clubs.club_membership import ClubMembership

    user = User.objects.create_user(
        username="blend_user", display_name="Blend User"
    )
    ClubMembership.objects.create(user=user, club=pharmacy_club, role="admin")
    return user


@pytest.fixture
def blend_pool():
    from cafe.models.rdlevels.blend_pool import BlendPool

    return BlendPool.objects.create(name="Test Pool", weighting_system="flat")


@pytest.fixture
def default_blend_pool():
    from cafe.models.rdlevels.blend_pool import BlendPool, DEFAULT_BLEND_POOL_ID

    pool, _ = BlendPool.objects.get_or_create(
        id=DEFAULT_BLEND_POOL_ID, defaults={"name": "Default Pool"}
    )
    return pool


@pytest.fixture
def blend_config():
    from cafe.models.rdlevels.daily_blend_configuration import DailyBlendConfiguration

    return DailyBlendConfiguration.get_config()


# ============== blend_pool_edit ==============


@pytest.mark.django_db
@patch("cafe.views.rdlevels.dailyblend.blend_pool_edit.report_blend_change")
def test_pool_edit_name_reports_change(mock_report, client, blend_user, blend_pool):
    client.force_login(blend_user)
    url = reverse("cafe:blend_pool_edit", args=[blend_pool.id])

    client.post(url, {"name": "Renamed Pool", "weighting_system": "flat"})

    mock_report.assert_called_once()
    payload = mock_report.call_args[0][0]
    assert "embeds" in payload


@pytest.mark.django_db
@patch("cafe.views.rdlevels.dailyblend.blend_pool_edit.report_blend_change")
def test_pool_edit_weighting_reports_change(
    mock_report, client, blend_user, blend_pool
):
    client.force_login(blend_user)
    url = reverse("cafe:blend_pool_edit", args=[blend_pool.id])

    client.post(url, {"name": blend_pool.name, "weighting_system": "aging"})

    mock_report.assert_called_once()
    payload = mock_report.call_args[0][0]
    assert "embeds" in payload


@pytest.mark.django_db
@patch("cafe.views.rdlevels.dailyblend.blend_pool_edit.report_blend_change")
def test_pool_edit_both_fields_reports_twice(
    mock_report, client, blend_user, blend_pool
):
    client.force_login(blend_user)
    url = reverse("cafe:blend_pool_edit", args=[blend_pool.id])

    client.post(url, {"name": "New Name", "weighting_system": "aging"})

    assert mock_report.call_count == 2


@pytest.mark.django_db
@patch("cafe.views.rdlevels.dailyblend.blend_pool_edit.report_blend_change")
def test_pool_edit_no_changes_no_report(mock_report, client, blend_user, blend_pool):
    client.force_login(blend_user)
    url = reverse("cafe:blend_pool_edit", args=[blend_pool.id])

    client.post(
        url, {"name": blend_pool.name, "weighting_system": blend_pool.weighting_system}
    )

    mock_report.assert_not_called()


# ============== blend_pool_delete ==============


@pytest.mark.django_db
@patch("cafe.views.rdlevels.dailyblend.blend_pool_delete.report_blend_change")
def test_pool_delete_reports_change(mock_report, client, blend_user, blend_pool):
    client.force_login(blend_user)
    url = reverse("cafe:blend_pool_delete", args=[blend_pool.id])

    client.post(url)

    mock_report.assert_called_once()
    payload = mock_report.call_args[0][0]
    assert "embeds" in payload


@pytest.mark.django_db
@patch("cafe.views.rdlevels.dailyblend.blend_pool_delete.report_blend_change")
def test_pool_delete_default_pool_no_report(
    mock_report, client, blend_user, default_blend_pool
):
    client.force_login(blend_user)
    url = reverse("cafe:blend_pool_delete", args=[default_blend_pool.id])

    client.post(url)

    mock_report.assert_not_called()


# ============== blend_pool (add/remove/ticket) ==============


@pytest.mark.django_db
@patch("cafe.views.rdlevels.dailyblend.blend_pool.report_blend_change")
def test_pool_add_level_reports_change(
    mock_report, client, blend_user, blend_pool, rdlevel
):
    client.force_login(blend_user)
    url = reverse("cafe:blend_pool", args=[blend_pool.id])

    client.post(url, {"level_id": rdlevel.id, "action": "add"})

    mock_report.assert_called_once()
    payload = mock_report.call_args[0][0]
    assert "embeds" in payload


@pytest.mark.django_db
@patch("cafe.views.rdlevels.dailyblend.blend_pool.report_blend_change")
def test_pool_add_level_twice_reports_once(
    mock_report, client, blend_user, blend_pool, rdlevel
):
    """Adding a level that's already in the pool should not report (get_or_create returns created=False)."""
    from cafe.models.rdlevels.blend_random_pool import DailyBlendRandomPool

    DailyBlendRandomPool.objects.create(level=rdlevel, pool=blend_pool)

    client.force_login(blend_user)
    url = reverse("cafe:blend_pool", args=[blend_pool.id])

    client.post(url, {"level_id": rdlevel.id, "action": "add"})

    mock_report.assert_not_called()


@pytest.mark.django_db
@patch("cafe.views.rdlevels.dailyblend.blend_pool.report_blend_change")
def test_pool_remove_level_reports_change(
    mock_report, client, blend_user, blend_pool, rdlevel
):
    from cafe.models.rdlevels.blend_random_pool import DailyBlendRandomPool

    DailyBlendRandomPool.objects.create(level=rdlevel, pool=blend_pool)

    client.force_login(blend_user)
    url = reverse("cafe:blend_pool", args=[blend_pool.id])

    client.post(url, {"level_id": rdlevel.id, "action": "remove"})

    mock_report.assert_called_once()
    payload = mock_report.call_args[0][0]
    assert "embeds" in payload


@pytest.mark.django_db
@patch("cafe.views.rdlevels.dailyblend.blend_pool.report_blend_change")
def test_pool_ticket_change_reports(
    mock_report, client, blend_user, blend_pool, rdlevel
):
    from cafe.models.rdlevels.blend_random_pool import DailyBlendRandomPool

    DailyBlendRandomPool.objects.create(level=rdlevel, pool=blend_pool)

    client.force_login(blend_user)
    url = reverse("cafe:blend_pool", args=[blend_pool.id])

    client.post(url, {"level_id": rdlevel.id, "action": "ticket", "tickets": 5})

    mock_report.assert_called_once()
    payload = mock_report.call_args[0][0]
    assert "embeds" in payload


@pytest.mark.django_db
@patch("cafe.views.rdlevels.dailyblend.blend_pool.report_blend_change")
def test_pool_ticket_missing_value_no_report(
    mock_report, client, blend_user, blend_pool, rdlevel
):
    from cafe.models.rdlevels.blend_random_pool import DailyBlendRandomPool

    DailyBlendRandomPool.objects.create(level=rdlevel, pool=blend_pool)

    client.force_login(blend_user)
    url = reverse("cafe:blend_pool", args=[blend_pool.id])

    client.post(url, {"level_id": rdlevel.id, "action": "ticket"})

    mock_report.assert_not_called()


# ============== blend_config ==============


@pytest.mark.django_db
@patch("cafe.views.rdlevels.dailyblend.blend_config.report_blend_change")
def test_config_pause_reports_change(mock_report, client, blend_user, blend_config):
    client.force_login(blend_user)
    url = reverse("cafe:blend_config")

    client.post(url, {
        "paused": "on",
        "webhook_urls": blend_config.webhook_urls,
        "jsonata_script": blend_config.jsonata_script,
        "reporting_webhook_url": blend_config.reporting_webhook_url,
    })

    mock_report.assert_called_once()
    payload = mock_report.call_args[0][0]
    assert "embeds" in payload


@pytest.mark.django_db
@patch("cafe.views.rdlevels.dailyblend.blend_config.report_blend_change")
def test_config_webhook_urls_reports_change(
    mock_report, client, blend_user, blend_config
):
    client.force_login(blend_user)
    url = reverse("cafe:blend_config")

    client.post(url, {
        "paused": "",
        "webhook_urls": "https://discord.com/api/webhooks/new",
        "jsonata_script": blend_config.jsonata_script,
        "reporting_webhook_url": blend_config.reporting_webhook_url,
    })

    mock_report.assert_called_once()


@pytest.mark.django_db
@patch("cafe.views.rdlevels.dailyblend.blend_config.report_blend_change")
def test_config_jsonata_reports_change(mock_report, client, blend_user, blend_config):
    client.force_login(blend_user)
    url = reverse("cafe:blend_config")

    client.post(url, {
        "paused": "",
        "webhook_urls": blend_config.webhook_urls,
        "jsonata_script": "$.content",
        "reporting_webhook_url": blend_config.reporting_webhook_url,
    })

    mock_report.assert_called_once()


@pytest.mark.django_db
@patch("cafe.views.rdlevels.dailyblend.blend_config.report_blend_change")
def test_config_reporting_url_reports_to_old_url(
    mock_report, client, blend_user, blend_config
):
    """When the reporting URL itself changes, the notification should go to the old URL."""
    blend_config.reporting_webhook_url = "https://discord.com/api/webhooks/old"
    blend_config.save()

    client.force_login(blend_user)
    url = reverse("cafe:blend_config")

    client.post(url, {
        "paused": "",
        "webhook_urls": blend_config.webhook_urls,
        "jsonata_script": blend_config.jsonata_script,
        "reporting_webhook_url": "https://discord.com/api/webhooks/new",
    })

    mock_report.assert_called_once()
    assert mock_report.call_args[1]["override_webhook_url"] == "https://discord.com/api/webhooks/old"


@pytest.mark.django_db
@patch("cafe.views.rdlevels.dailyblend.blend_config.report_blend_change")
def test_config_multiple_changes_report_each(
    mock_report, client, blend_user, blend_config
):
    client.force_login(blend_user)
    url = reverse("cafe:blend_config")

    client.post(url, {
        "paused": "on",
        "webhook_urls": "https://discord.com/api/webhooks/changed",
        "jsonata_script": "$.new_script",
        "reporting_webhook_url": blend_config.reporting_webhook_url,
    })

    # paused + webhook_urls + jsonata = 3 calls
    assert mock_report.call_count == 3


@pytest.mark.django_db
@patch("cafe.views.rdlevels.dailyblend.blend_config.report_blend_change")
def test_config_no_changes_no_report(mock_report, client, blend_user, blend_config):
    client.force_login(blend_user)
    url = reverse("cafe:blend_config")

    client.post(url, {
        "paused": "",
        "webhook_urls": blend_config.webhook_urls,
        "jsonata_script": blend_config.jsonata_script,
        "reporting_webhook_url": blend_config.reporting_webhook_url,
    })

    mock_report.assert_not_called()


# ============== blend_schedule ==============


@pytest.mark.django_db
@patch("cafe.views.rdlevels.dailyblend.blend_schedule.report_blend_change")
def test_schedule_set_level_reports_change(
    mock_report, client, blend_user, rdlevel
):
    client.force_login(blend_user)
    url = reverse("cafe:blend_schedule")

    client.post(url, {
        "featured_date": "2026-07-01",
        "level_or_pool_id": rdlevel.id,
    })

    mock_report.assert_called_once()
    payload = mock_report.call_args[0][0]
    assert "embeds" in payload


@pytest.mark.django_db
@patch("cafe.views.rdlevels.dailyblend.blend_schedule.report_blend_change")
def test_schedule_set_pool_reports_change(
    mock_report, client, blend_user, blend_pool
):
    client.force_login(blend_user)
    url = reverse("cafe:blend_schedule")

    client.post(url, {
        "featured_date": "2026-07-01",
        "level_or_pool_id": blend_pool.id,
    })

    mock_report.assert_called_once()
    payload = mock_report.call_args[0][0]
    assert "embeds" in payload


@pytest.mark.django_db
@patch("cafe.views.rdlevels.dailyblend.blend_schedule.report_blend_change")
def test_schedule_clear_reports_change(mock_report, client, blend_user, rdlevel):
    from cafe.models.rdlevels.daily_blend import DailyBlend

    DailyBlend.objects.create(
        level=rdlevel, featured_date=datetime.date(2026, 7, 1)
    )

    client.force_login(blend_user)
    url = reverse("cafe:blend_schedule")

    client.post(url, {
        "featured_date": "2026-07-01",
        "level_or_pool_id": "",
    })

    mock_report.assert_called_once()
    payload = mock_report.call_args[0][0]
    assert "embeds" in payload


@pytest.mark.django_db
@patch("cafe.views.rdlevels.dailyblend.blend_schedule.report_blend_change")
def test_schedule_invalid_level_no_report(mock_report, client, blend_user):
    client.force_login(blend_user)
    url = reverse("cafe:blend_schedule")

    client.post(url, {
        "featured_date": "2026-07-01",
        "level_or_pool_id": "rnonexistent",
    })

    mock_report.assert_not_called()


@pytest.mark.django_db
@patch("cafe.views.rdlevels.dailyblend.blend_schedule.report_blend_change")
def test_schedule_invalid_pool_no_report(mock_report, client, blend_user):
    client.force_login(blend_user)
    url = reverse("cafe:blend_schedule")

    client.post(url, {
        "featured_date": "2026-07-01",
        "level_or_pool_id": "bnonexistent",
    })

    mock_report.assert_not_called()
