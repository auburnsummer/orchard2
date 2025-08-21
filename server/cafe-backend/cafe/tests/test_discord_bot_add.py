import uuid
from conftest import create_discord_request
import pytest

def make_discord_body(
    delegated: bool, guild_id: str, attachments: list[str], author: dict, invoker: dict, is_webhook: bool = False
):
    name = "Add to Rhythm Café (delegated)" if delegated else "Add to Rhythm Café"
    data = {
        "type": 2,
        "version": 1,
        "guild": {"id": guild_id},
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


@pytest.mark.django_db
def test_add_returns_no_group_response_if_server_has_no_connected_group(
    client_with_discord_key,
):
    client, private_key = client_with_discord_key
    body = make_discord_body(
        False,
        "01234567890",
        [],
        {
            "id": "297727909609603083",
            "global_name": "auburn",
            "username": "auburnsummer",
        },
        {
            "id": "297727909609603083",
            "global_name": "auburn",
            "username": "auburnsummer",
        },
    )
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
    body = make_discord_body(
        False,
        discord_guild_with_attached_club.id,
        [],
        {
            "id": "297727909609603083",
            "global_name": "auburn",
            "username": "auburnsummer",
        },
        {
            "id": "297727909609603083",
            "global_name": "auburn",
            "username": "auburnsummer",
        },
    )
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
def test_add_returns_only_self_messages_response_if_user_is_not_poster(
    client_with_discord_key, discord_guild_with_attached_club
):
    client, private_key = client_with_discord_key
    body = make_discord_body(
        False,
        discord_guild_with_attached_club.id,
        ["file.rdzip"],
        {
            "id": "12423412342343444",
            "global_name": "someone else",
            "username": "someone",
        },
        {
            "id": "297727909609603083",
            "global_name": "auburn",
            "username": "auburnsummer",
        },
    )
    request = create_discord_request(body, private_key)
    response = client.post("/discord_interactions/", **request)
    assert response.status_code == 200
    assert response.json() == {
        "data": {
            "content": "You can only add levels from your own messages.",
            "flags": 64,
        },
        "type": 4,
    }

@pytest.mark.django_db
def test_add_returns_only_self_messages_response_if_message_is_from_webhook(
    client_with_discord_key, discord_guild_with_attached_club
):
    client, private_key = client_with_discord_key
    body = make_discord_body(
        False,
        discord_guild_with_attached_club.id,
        ["file.rdzip"],
        {
            "id": "12423412342343444",
            "global_name": "someone else",
            "username": "someone",
        },
        {
            "id": "297727909609603083",
            "global_name": "auburn",
            "username": "auburnsummer",
        },
        is_webhook=True
    )
    request = create_discord_request(body, private_key)
    response = client.post("/discord_interactions/", **request)
    assert response.status_code == 200
    assert response.json() ==  {'data': {'content': "You can't add levels from webhooks.", 'flags': 64},
   'type': 4}


@pytest.mark.django_db
def test_add_returns_line_for_each_rdzip_attachment(
    client_with_discord_key, discord_guild_with_attached_club
):
    client, private_key = client_with_discord_key
    body = make_discord_body(
        False,
        discord_guild_with_attached_club.id,
        ["level1.rdzip", "level2.rdzip", "level3.rdzip"],
        {
            "id": "297727909609603083",
            "global_name": "auburn",
            "username": "auburnsummer",
        },
        {
            "id": "297727909609603083",
            "global_name": "auburn",
            "username": "auburnsummer",
        },
    )
    request = create_discord_request(body, private_key)
    response = client.post("/discord_interactions/", **request)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["type"] == 4
    assert response_data["data"]["flags"] == 64
    content = response_data["data"]["content"]
    
    # Should have 3 lines for 3 attachments
    lines = content.split("\n")
    assert len(lines) == 3
    
    # Each line should have the filename and a link
    assert "level1.rdzip" in lines[0]
    assert "level2.rdzip" in lines[1]
    assert "level3.rdzip" in lines[2]
    
    # Each line should contain a clickable link
    for line in lines:
        assert "click here" in line
        assert "(" in line and ")" in line  # Markdown link format


@pytest.mark.django_db
def test_resulting_level_portal_link_is_valid(
    client_with_discord_key, discord_guild_with_attached_club
):
    from django.core.signing import TimestampSigner, BadSignature
    from django.urls import reverse
    from orchard.settings import DOMAIN_URL
    
    client, private_key = client_with_discord_key
    body = make_discord_body(
        False,
        discord_guild_with_attached_club.id,
        ["test.rdzip"],
        {
            "id": "297727909609603083",
            "global_name": "auburn",
            "username": "auburnsummer",
        },
        {
            "id": "297727909609603083",
            "global_name": "auburn",
            "username": "auburnsummer",
        },
    )
    request = create_discord_request(body, private_key)
    response = client.post("/discord_interactions/", **request)
    assert response.status_code == 200
    response_data = response.json()
    content = response_data["data"]["content"]
    
    # Extract the URL from the markdown link
    import re
    url_match = re.search(r'\[click here\]\(([^)]+)\)', content)
    assert url_match is not None
    full_url = url_match.group(1)
    
    # Verify the URL starts with the domain
    assert full_url.startswith(DOMAIN_URL)
    
    # Extract the secret from the URL
    url_path = full_url.replace(DOMAIN_URL, "")
    secret_match = re.search(r'/levels/add/([^/]+)/', url_path)
    assert secret_match is not None
    secret = secret_match.group(1)
    
    # Verify the secret can be decoded with the correct signer
    addlevel_signer = TimestampSigner(salt="addlevel")
    try:
        payload = addlevel_signer.unsign_object(secret)
        # Verify the payload contains expected data
        assert payload["level_url"] == "https://example.com/test.rdzip"
        assert payload["discord_user_id"] == "297727909609603083"
        assert payload["discord_user_name_hint"] == "auburn"
        assert payload["club_id"] == discord_guild_with_attached_club.club.id
    except BadSignature:
        pytest.fail("Level portal URL contains invalid signature")


@pytest.mark.django_db
def test_add_delegated_allows_webhooks(
    client_with_discord_key, discord_guild_with_attached_club
):
    client, private_key = client_with_discord_key
    body = make_discord_body(
        True,  # delegated=True
        discord_guild_with_attached_club.id,
        ["webhook-level.rdzip"],
        {
            "id": "12423412342343444",
            "global_name": "webhook bot",
            "username": "webhookbot",
        },
        {
            "id": "297727909609603083",
            "global_name": "auburn",
            "username": "auburnsummer",
        },
        is_webhook=True
    )
    request = create_discord_request(body, private_key)
    response = client.post("/discord_interactions/", **request)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["type"] == 4
    assert response_data["data"]["flags"] == 64
    content = response_data["data"]["content"]
    
    # Should succeed and return a link, not an error
    assert "webhook-level.rdzip" in content
    assert "click here" in content
    assert "You can't add levels from webhooks" not in content


@pytest.mark.django_db
def test_add_delegated_allows_other_users_messages(
    client_with_discord_key, discord_guild_with_attached_club
):
    client, private_key = client_with_discord_key
    body = make_discord_body(
        True,  # delegated=True
        discord_guild_with_attached_club.id,
        ["other-user-level.rdzip"],
        {
            "id": "12423412342343444",
            "global_name": "someone else",
            "username": "someone",
        },
        {
            "id": "297727909609603083",
            "global_name": "auburn",
            "username": "auburnsummer",
        },
    )
    request = create_discord_request(body, private_key)
    response = client.post("/discord_interactions/", **request)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["type"] == 4
    assert response_data["data"]["flags"] == 64
    content = response_data["data"]["content"]
    
    # Should succeed and return a link, not an error
    assert "other-user-level.rdzip" in content
    assert "click here" in content
    assert "You can only add levels from your own messages" not in content
