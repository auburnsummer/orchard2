import json
from conftest import create_discord_request


def test_discord_bot_entry_returns_401_on_missing_headers(client):
    """Test that missing Discord headers return 401."""
    response = client.post('/discord_interactions/', 
                          data=json.dumps({'type': 1}),
                          content_type='application/json')
    
    assert response.status_code == 401
    assert response.content == b'Discord headers missing.'


def test_discord_bot_entry_returns_401_on_missing_signature_header(client_with_discord_key):
    """Test that missing signature header returns 401."""
    client, private_key = client_with_discord_key
    
    response = client.post('/discord_interactions/',
                          data=json.dumps({'type': 1}),
                          content_type='application/json',
                          HTTP_X_SIGNATURE_TIMESTAMP='1234567890')
    
    assert response.status_code == 401
    assert response.content == b'Discord headers missing.'


def test_discord_bot_entry_returns_401_on_missing_timestamp_header(client_with_discord_key):
    """Test that missing timestamp header returns 401."""
    client, private_key = client_with_discord_key
    
    response = client.post('/discord_interactions/',
                          data=json.dumps({'type': 1}),
                          content_type='application/json',
                          HTTP_X_SIGNATURE_ED25519='fakesignature')
    
    assert response.status_code == 401
    assert response.content == b'Discord headers missing.'


def test_discord_bot_entry_returns_401_on_invalid_signature(client_with_discord_key):
    """Test that invalid signature returns 401."""
    client, private_key = client_with_discord_key
    
    response = client.post('/discord_interactions/',
                          data=json.dumps({'type': 1}),
                          content_type='application/json',
                          HTTP_X_SIGNATURE_ED25519='0123456789abcdef' * 8,  # 64 char hex but invalid
                          HTTP_X_SIGNATURE_TIMESTAMP='1234567890')
    
    assert response.status_code == 401
    assert response.content == b'Signature is incorrect.'


def test_discord_bot_entry_ping(client_with_discord_key):
    """Test Discord ping interaction (type 1)."""
    client, private_key = client_with_discord_key
    
    ping_payload = {'type': 1}
    request_data = create_discord_request(ping_payload, private_key)
    
    response = client.post('/discord_interactions/', **request_data)
    
    assert response.status_code == 200
    response_data = response.json()
    assert response_data == {'type': 1}


def test_discord_bot_entry_unknown_command(client_with_discord_key):
    """Test unknown command handling."""
    client, private_key = client_with_discord_key
    
    command_payload = {
        'type': 2,
        'data': {
            'name': 'nonexistent_command'
        }
    }
    request_data = create_discord_request(command_payload, private_key)
    
    response = client.post('/discord_interactions/', **request_data)
    
    assert response.status_code == 200
    response_data = response.json()
    # Should return an ephemeral response about unknown command
    assert response_data['type'] == 4  # CHANNEL_MESSAGE_WITH_SOURCE
    assert response_data['data']['flags'] == 64  # EPHEMERAL
    assert 'Unknown command: nonexistent_command' in response_data['data']['content']


def test_discord_bot_entry_unknown_type(client_with_discord_key):
    """Test handling of unknown interaction type."""
    client, private_key = client_with_discord_key
    
    unknown_payload = {'type': 99}  # Unknown type
    request_data = create_discord_request(unknown_payload, private_key)
    
    response = client.post('/discord_interactions/', **request_data)
    
    assert response.status_code == 404
    assert response.content == b'Not sure how to handle this type.'


# each command will get its own test file