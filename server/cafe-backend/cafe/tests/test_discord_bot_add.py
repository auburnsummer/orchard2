import uuid
from unittest.mock import patch

from conftest import create_discord_request
import pytest

from cafe.models.add_session import AddSession, AddSessionPhase
from cafe.views.discord_bot.handlers.utils import Flags, ResponseType


def make_discord_body(
    delegated: bool, guild_id: str, attachments: list[str], author: dict, invoker: dict, is_webhook: bool = False
):
    """Build an APPLICATION_COMMAND (type 2) payload for the add command."""
    name = "Add to Rhythm Café (delegated)" if delegated else "Add to Rhythm Café"
    data = {
        "type": 2,
        "id": str(uuid.uuid4()),
        "token": "test_interaction_token",
        "version": 1,
        "guild": {"id": guild_id},
        "authorizing_integration_owners": {"0": guild_id},
        "data": {
            "id": "1289938243097333825",
            "name": name,
            "resolved": {
                "messages": {
                    "1378335040420712612": {
                        "attachments": [
                            {
                                "filename": attachment,
                                "id": str(uuid.uuid4()),
                                "url": f"https://example.com/{attachment}",
                                "proxy_url": f"https://proxy.example.com/{attachment}",
                                "size": 1234,
                                "content_scan_version": 1,
                            }
                            for attachment in attachments
                        ],
                        "author": author,
                    }
                }
            },
            "target_id": "1378335040420712612",
        },
        "member": {"user": invoker},
    }
    if is_webhook:
        data["data"]["resolved"]["messages"]["1378335040420712612"]["webhook_id"] = str(uuid.uuid4())
    return data


def make_component_interaction(session_id, guild_id, custom_id, values=None, delegated=False):
    """Build a MESSAGE_COMPONENT (type 3) payload for add_step."""
    name = "Add to Rhythm Café (delegated)" if delegated else "Add to Rhythm Café"
    data = {
        "type": 3,
        "id": str(uuid.uuid4()),
        "token": "test_followup_token",
        "guild": {"id": guild_id},
        "authorizing_integration_owners": {"0": guild_id},
        "message": {
            "interaction": {
                "id": session_id,
                "name": name,
            }
        },
        "member": {"user": {"id": "297727909609603083"}},
        "data": {
            "custom_id": custom_id,
        },
    }
    if values is not None:
        data["data"]["values"] = values
    return data


def make_modal_submit(session_id, guild_id, level_id_value, overwrite_metadata=False, delegated=False):
    """Build a MODAL_SUBMIT (type 5) payload for the update modal."""
    name = "Add to Rhythm Café (delegated)" if delegated else "Add to Rhythm Café"
    return {
        "type": 5,
        "id": str(uuid.uuid4()),
        "token": "test_modal_token",
        "guild": {"id": guild_id},
        "authorizing_integration_owners": {"0": guild_id},
        "message": {
            "interaction": {
                "id": session_id,
                "name": name,
            }
        },
        "member": {"user": {"id": "297727909609603083"}},
        "data": {
            "custom_id": "update_modal",
            "components": [
                {},  # text component at index 0
                {"component": {"value": level_id_value}},  # label+text_input at index 1
                {"component": {"value": overwrite_metadata}},  # checkbox at index 2
            ],
        },
    }


def _extract_custom_ids(components):
    """Recursively extract all custom_ids from nested Discord components."""
    ids = []
    for c in components:
        if "custom_id" in c:
            ids.append(c["custom_id"])
        if "components" in c:
            ids.extend(_extract_custom_ids(c["components"]))
    return ids


def _create_session(guild_id, phase=AddSessionPhase.SELECTING_TYPE, add_type="new",
                    attachments=None, selected_url=None):
    """Helper to directly create an AddSession for step tests."""
    from cafe.models.user import User
    user = User.objects.create_user(username=f"testuser_{uuid.uuid4().hex[:8]}")
    if attachments is None:
        attachments = [{"id": "att1", "filename": "level.rdzip", "url": "https://example.com/level.rdzip"}]
    session_id = f"session_{uuid.uuid4().hex[:12]}"
    return AddSession.objects.create(
        id=session_id,
        user=user,
        interaction_token="test_token",
        phase=phase,
        attachments=attachments,
        selected_attachment_url=selected_url or (attachments[0]["url"] if attachments else None),
        add_type=add_type,
    )


def _create_rdlevel(submitter, club):
    """Helper to create a test RDLevel with the given submitter."""
    from cafe.models.rdlevels.rdlevel import RDLevel
    from django.utils import timezone
    with patch("cafe.models.rdlevels.rdlevel.sync_level_to_typesense"):
        return RDLevel.objects.create(
            artist="Test Artist",
            artist_tokens=["test"],
            artist_raw="Test Artist",
            song="Test Song",
            song_alt="",
            song_raw="Test Song",
            seizure_warning=False,
            description="test",
            hue=0.0,
            authors=["Test"],
            authors_raw="Test",
            max_bpm=120,
            min_bpm=60,
            difficulty=1,
            single_player=True,
            two_player=False,
            last_updated=timezone.now(),
            tags=[],
            sha1=f"sha1_{uuid.uuid4().hex}",
            rdlevel_sha1=f"rdsha1_{uuid.uuid4().hex}",
            rd_md5=f"md5_{uuid.uuid4().hex}",
            is_animated=False,
            rdzip_url="https://example.com/test.rdzip",
            image_url="https://example.com/image.jpg",
            thumb_url="https://example.com/thumb.jpg",
            icon_url="",
            submitter=submitter,
            club=club,
            approval=0,
        )


COMPONENTS_V2_FLAGS = Flags.IS_COMPONENTS_V2.value | Flags.EPHEMERAL.value

SAME_USER_AUTHOR = {"id": "297727909609603083", "global_name": "auburn", "username": "auburnsummer"}
SAME_USER_INVOKER = {"id": "297727909609603083", "global_name": "auburn", "username": "auburnsummer"}
DIFFERENT_AUTHOR = {"id": "12423412342343444", "global_name": "someone else", "username": "someone"}


# ---- Error cases ----

@pytest.mark.django_db
def test_add_returns_no_group_response_if_server_has_no_connected_group(
    client_with_discord_key,
):
    client, private_key = client_with_discord_key
    body = make_discord_body(False, "01234567890", [], SAME_USER_AUTHOR, SAME_USER_INVOKER)
    request = create_discord_request(body, private_key)
    response = client.post("/discord_interactions/", **request)
    assert response.status_code == 200
    assert response.json() == {
        "data": {
            "content": "No group found for this server (the server owner needs "
            "to use the `/connectgroup` command)",
            "flags": 64,
        },
        "type": 4,
    }


@pytest.mark.django_db
def test_add_returns_no_rdzips_response_if_message_has_no_attachments_ending_with_rdzip(
    client_with_discord_key, discord_guild_with_attached_club
):
    client, private_key = client_with_discord_key
    body = make_discord_body(False, discord_guild_with_attached_club.id, [], SAME_USER_AUTHOR, SAME_USER_INVOKER)
    request = create_discord_request(body, private_key)
    response = client.post("/discord_interactions/", **request)
    assert response.status_code == 200
    assert response.json() == {
        "data": {
            "content": "The post doesn't have any attachments ending with " ".rdzip!",
            "flags": 64,
        },
        "type": 4,
    }


@pytest.mark.django_db
def test_add_rejects_other_users_messages(
    client_with_discord_key, discord_guild_with_attached_club
):
    client, private_key = client_with_discord_key
    body = make_discord_body(
        False, discord_guild_with_attached_club.id, ["file.rdzip"],
        DIFFERENT_AUTHOR, SAME_USER_INVOKER,
    )
    request = create_discord_request(body, private_key)
    response = client.post("/discord_interactions/", **request)
    assert response.status_code == 200
    assert response.json() == {
        "data": {"content": "You can only add levels from your own messages.", "flags": 64},
        "type": 4,
    }


@pytest.mark.django_db
def test_add_rejects_webhook_messages(
    client_with_discord_key, discord_guild_with_attached_club
):
    client, private_key = client_with_discord_key
    body = make_discord_body(
        False, discord_guild_with_attached_club.id, ["file.rdzip"],
        DIFFERENT_AUTHOR, SAME_USER_INVOKER, is_webhook=True,
    )
    request = create_discord_request(body, private_key)
    response = client.post("/discord_interactions/", **request)
    assert response.status_code == 200
    assert response.json() == {
        "data": {"content": "You can't add levels from webhooks.", "flags": 64},
        "type": 4,
    }


# ---- Initial add_v2 response ----

@pytest.mark.django_db
def test_add_single_attachment_creates_session_at_selecting_type(
    client_with_discord_key, discord_guild_with_attached_club
):
    client, private_key = client_with_discord_key
    body = make_discord_body(
        False, discord_guild_with_attached_club.id, ["level.rdzip"],
        SAME_USER_AUTHOR, SAME_USER_INVOKER,
    )
    request = create_discord_request(body, private_key)
    response = client.post("/discord_interactions/", **request)
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == ResponseType.CHANNEL_MESSAGE_WITH_SOURCE.value
    assert data["data"]["flags"] == COMPONENTS_V2_FLAGS

    # Session should be created at SELECTING_TYPE with attachment pre-selected
    session = AddSession.objects.get(id=body["id"])
    assert session.phase == AddSessionPhase.SELECTING_TYPE
    assert session.selected_attachment_url == "https://example.com/level.rdzip"

    # Should show type selector, not attachment selector
    custom_ids = _extract_custom_ids(data["data"]["components"])
    assert "p2_type_select" in custom_ids
    assert "p1_select_attachment" not in custom_ids


@pytest.mark.django_db
def test_add_multiple_attachments_creates_session_at_selecting_attachment(
    client_with_discord_key, discord_guild_with_attached_club
):
    client, private_key = client_with_discord_key
    body = make_discord_body(
        False, discord_guild_with_attached_club.id,
        ["level1.rdzip", "level2.rdzip", "level3.rdzip"],
        SAME_USER_AUTHOR, SAME_USER_INVOKER,
    )
    request = create_discord_request(body, private_key)
    response = client.post("/discord_interactions/", **request)
    assert response.status_code == 200
    data = response.json()

    session = AddSession.objects.get(id=body["id"])
    assert session.phase == AddSessionPhase.SELECTING_ATTACHMENT
    assert len(session.attachments) == 3

    # Should show attachment selector but not type selector yet
    custom_ids = _extract_custom_ids(data["data"]["components"])
    assert "p1_select_attachment" in custom_ids
    assert "p2_type_select" not in custom_ids


# ---- Delegated ----

@pytest.mark.django_db
def test_add_delegated_allows_webhooks(
    client_with_discord_key, discord_guild_with_attached_club
):
    client, private_key = client_with_discord_key
    body = make_discord_body(
        True, discord_guild_with_attached_club.id, ["webhook-level.rdzip"],
        {"id": "12423412342343444", "global_name": "webhook bot", "username": "webhookbot"},
        SAME_USER_INVOKER, is_webhook=True,
    )
    request = create_discord_request(body, private_key)
    response = client.post("/discord_interactions/", **request)
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == ResponseType.CHANNEL_MESSAGE_WITH_SOURCE.value
    assert data["data"]["flags"] == COMPONENTS_V2_FLAGS

    # Should create a session (not return an error)
    session = AddSession.objects.get(id=body["id"])
    assert session.phase in (AddSessionPhase.SELECTING_ATTACHMENT, AddSessionPhase.SELECTING_TYPE)


@pytest.mark.django_db
def test_add_delegated_allows_other_users_messages(
    client_with_discord_key, discord_guild_with_attached_club
):
    client, private_key = client_with_discord_key
    body = make_discord_body(
        True, discord_guild_with_attached_club.id, ["other-user-level.rdzip"],
        DIFFERENT_AUTHOR, SAME_USER_INVOKER,
    )
    request = create_discord_request(body, private_key)
    response = client.post("/discord_interactions/", **request)
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == ResponseType.CHANNEL_MESSAGE_WITH_SOURCE.value
    assert data["data"]["flags"] == COMPONENTS_V2_FLAGS

    session = AddSession.objects.get(id=body["id"])
    assert session.phase == AddSessionPhase.SELECTING_TYPE


# ---- Step interactions ----

@pytest.mark.django_db
def test_step_select_attachment_advances_to_selecting_type(
    client_with_discord_key, discord_guild_with_attached_club
):
    client, private_key = client_with_discord_key
    guild_id = discord_guild_with_attached_club.id
    attachments = [
        {"id": "att1", "filename": "level1.rdzip", "url": "https://example.com/level1.rdzip"},
        {"id": "att2", "filename": "level2.rdzip", "url": "https://example.com/level2.rdzip"},
    ]
    session = _create_session(guild_id, phase=AddSessionPhase.SELECTING_ATTACHMENT,
                              attachments=attachments, selected_url=None)

    body = make_component_interaction(session.id, guild_id, "p1_select_attachment", values=["att2"])
    request = create_discord_request(body, private_key)
    response = client.post("/discord_interactions/", **request)
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == ResponseType.UPDATE_ORIGINAL_MESSAGE.value

    session.refresh_from_db()
    assert session.phase == AddSessionPhase.SELECTING_TYPE
    assert session.selected_attachment_url == "https://example.com/level2.rdzip"

    custom_ids = _extract_custom_ids(data["data"]["components"])
    assert "p2_type_select" in custom_ids


@pytest.mark.django_db
def test_step_select_type_new_shows_submit_buttons(
    client_with_discord_key, discord_guild_with_attached_club
):
    client, private_key = client_with_discord_key
    guild_id = discord_guild_with_attached_club.id
    session = _create_session(guild_id)

    body = make_component_interaction(session.id, guild_id, "p2_type_select", values=["new"])
    request = create_discord_request(body, private_key)
    response = client.post("/discord_interactions/", **request)
    assert response.status_code == 200
    data = response.json()

    session.refresh_from_db()
    assert session.add_type == "new"

    custom_ids = _extract_custom_ids(data["data"]["components"])
    assert "p2_new_submit" in custom_ids
    assert "p2_new_submit_edit" in custom_ids


@pytest.mark.django_db
def test_step_select_type_update_shows_update_button(
    client_with_discord_key, discord_guild_with_attached_club
):
    client, private_key = client_with_discord_key
    guild_id = discord_guild_with_attached_club.id
    session = _create_session(guild_id)

    body = make_component_interaction(session.id, guild_id, "p2_type_select", values=["update"])
    request = create_discord_request(body, private_key)
    response = client.post("/discord_interactions/", **request)
    assert response.status_code == 200
    data = response.json()

    session.refresh_from_db()
    assert session.add_type == "update"

    custom_ids = _extract_custom_ids(data["data"]["components"])
    assert "p2_update_submit" in custom_ids


@pytest.mark.django_db
@patch("cafe.views.discord_bot.handlers.add.run_prefill_v2")
def test_step_submit_new_creates_prefill_and_starts_task(
    mock_prefill, client_with_discord_key, discord_guild_with_attached_club
):
    from cafe.models.rdlevels.prefill import RDLevelPrefillResult
    client, private_key = client_with_discord_key
    guild_id = discord_guild_with_attached_club.id
    session = _create_session(guild_id, add_type="new")

    body = make_component_interaction(session.id, guild_id, "p2_new_submit")
    request = create_discord_request(body, private_key)
    response = client.post("/discord_interactions/", **request)
    assert response.status_code == 200
    data = response.json()

    session.refresh_from_db()
    assert session.phase == AddSessionPhase.UPLOADING

    # Should show uploading message
    assert any("Uploading" in str(c.get("content", "")) for c in data["data"]["components"])

    # Prefill should be created with correct params
    prefill = RDLevelPrefillResult.objects.last()
    assert prefill is not None
    assert prefill.go_to_prepost is False
    assert prefill.prefill_type == "new"
    assert prefill.url == "https://example.com/level.rdzip"
    assert prefill.club == discord_guild_with_attached_club.club
    mock_prefill.assert_called_once_with(prefill.id, session.id)


@pytest.mark.django_db
@patch("cafe.views.discord_bot.handlers.add.run_prefill_v2")
def test_step_submit_new_edit_creates_prefill_with_prepost(
    mock_prefill, client_with_discord_key, discord_guild_with_attached_club
):
    from cafe.models.rdlevels.prefill import RDLevelPrefillResult
    client, private_key = client_with_discord_key
    guild_id = discord_guild_with_attached_club.id
    session = _create_session(guild_id, add_type="new")

    body = make_component_interaction(session.id, guild_id, "p2_new_submit_edit")
    request = create_discord_request(body, private_key)
    response = client.post("/discord_interactions/", **request)
    assert response.status_code == 200

    session.refresh_from_db()
    assert session.phase == AddSessionPhase.UPLOADING

    prefill = RDLevelPrefillResult.objects.last()
    assert prefill is not None
    assert prefill.go_to_prepost is True
    assert prefill.prefill_type == "new"
    mock_prefill.assert_called_once_with(prefill.id, session.id)


@pytest.mark.django_db
def test_step_update_submit_returns_modal(
    client_with_discord_key, discord_guild_with_attached_club
):
    client, private_key = client_with_discord_key
    guild_id = discord_guild_with_attached_club.id
    session = _create_session(guild_id, add_type="update")

    body = make_component_interaction(session.id, guild_id, "p2_update_submit")
    request = create_discord_request(body, private_key)
    response = client.post("/discord_interactions/", **request)
    assert response.status_code == 200
    data = response.json()

    assert data["type"] == ResponseType.MODAL.value
    assert data["data"]["custom_id"] == "update_modal"


@pytest.mark.django_db
@patch("cafe.views.discord_bot.handlers.add.run_prefill_v2")
def test_step_update_modal_with_valid_level_starts_task(
    mock_prefill, client_with_discord_key, discord_guild_with_attached_club
):
    from cafe.models.rdlevels.prefill import RDLevelPrefillResult
    client, private_key = client_with_discord_key
    guild_id = discord_guild_with_attached_club.id
    club = discord_guild_with_attached_club.club
    session = _create_session(guild_id, add_type="update")

    # Create a level owned by the session's user so they have permission
    level = _create_rdlevel(session.user, club)

    body = make_modal_submit(session.id, guild_id, level.id)
    request = create_discord_request(body, private_key)
    response = client.post("/discord_interactions/", **request)
    assert response.status_code == 200

    session.refresh_from_db()
    assert session.phase == AddSessionPhase.UPLOADING

    prefill = RDLevelPrefillResult.objects.last()
    assert prefill is not None
    assert prefill.prefill_type == "update"
    assert prefill.level == level
    assert prefill.overwrite_metadata is False
    mock_prefill.assert_called_once_with(prefill.id, session.id)


@pytest.mark.django_db
def test_step_update_modal_with_nonexistent_level_shows_error(
    client_with_discord_key, discord_guild_with_attached_club
):
    client, private_key = client_with_discord_key
    guild_id = discord_guild_with_attached_club.id
    session = _create_session(guild_id, add_type="update")

    body = make_modal_submit(session.id, guild_id, "nonexistent_id")
    request = create_discord_request(body, private_key)
    response = client.post("/discord_interactions/", **request)
    assert response.status_code == 200

    session.refresh_from_db()
    assert session.phase == AddSessionPhase.ERROR_LEVEL_NOT_FOUND


@pytest.mark.django_db
def test_step_update_modal_with_no_permission_shows_error(
    client_with_discord_key, discord_guild_with_attached_club
):
    from cafe.models.user import User
    client, private_key = client_with_discord_key
    guild_id = discord_guild_with_attached_club.id
    club = discord_guild_with_attached_club.club
    session = _create_session(guild_id, add_type="update")

    # Create a level owned by a DIFFERENT user
    other_user = User.objects.create_user(username="other_user")
    level = _create_rdlevel(other_user, club)

    body = make_modal_submit(session.id, guild_id, level.id)
    request = create_discord_request(body, private_key)
    response = client.post("/discord_interactions/", **request)
    assert response.status_code == 200

    session.refresh_from_db()
    assert session.phase == AddSessionPhase.ERROR_NO_PERMISSION


@pytest.mark.django_db
@patch("cafe.views.discord_bot.handlers.add.run_prefill_v2")
def test_step_update_modal_with_overwrite_metadata_sets_flag(
    mock_prefill, client_with_discord_key, discord_guild_with_attached_club
):
    from cafe.models.rdlevels.prefill import RDLevelPrefillResult
    client, private_key = client_with_discord_key
    guild_id = discord_guild_with_attached_club.id
    club = discord_guild_with_attached_club.club
    session = _create_session(guild_id, add_type="update")

    level = _create_rdlevel(session.user, club)

    body = make_modal_submit(session.id, guild_id, level.id, overwrite_metadata=True)
    request = create_discord_request(body, private_key)
    response = client.post("/discord_interactions/", **request)
    assert response.status_code == 200

    prefill = RDLevelPrefillResult.objects.last()
    assert prefill is not None
    assert prefill.overwrite_metadata is True
    mock_prefill.assert_called_once_with(prefill.id, session.id)
