from conftest import create_discord_request

def test_version_returns_the_version(client_with_discord_key):
    client, private_key = client_with_discord_key
    command_data = {
        "data": {
            "id": "1245307952059912233",
            "name": "version",
            "type": 1,
        },
        "type": 2,
        "version": 1,
    }
    req = create_discord_request(command_data, private_key)
    response = client.post('/discord_interactions/', **req)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['type'] == 4
    assert response_data['data']['flags'] == 64
