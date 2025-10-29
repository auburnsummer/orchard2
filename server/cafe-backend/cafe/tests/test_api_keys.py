import pytest
from django.test import Client
from cafe.models.user import User


# API Key Management Views Tests

@pytest.mark.django_db
def test_api_key_view_requires_login(client: Client):
    """Test that the API key view requires authentication"""
    response = client.get('/accounts/profile/api-key/')
    assert response.status_code == 302
    assert '/accounts/login/' in response.url


@pytest.mark.django_db
def test_api_key_view_shows_no_key_initially(bridge_client: Client, user_with_no_clubs):
    """Test that initially users have no API key"""
    bridge_client.force_login(user_with_no_clubs)
    response = bridge_client.get('/accounts/profile/api-key/')
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['props']['hasApiKey'] is False
    # Note: apiKey is not returned in the view response since keys are hashed


@pytest.mark.django_db
def test_generate_api_key(bridge_client: Client, user_with_no_clubs):
    """Test generating a new API key"""
    bridge_client.force_login(user_with_no_clubs)
    
    # Generate API key
    response = bridge_client.post('/accounts/profile/api-key/generate/')
    assert response.status_code == 200
    response_data = response.json()
    
    # Check response structure
    assert response_data['props']['hasApiKey'] is True
    assert response_data['props']['apiKey'] is not None
    assert len(response_data['props']['apiKey']) > 0
    
    # Check success message
    assert len(response_data['messages']) == 1
    assert response_data['messages'][0]['level'] == 'success'
    assert 'API key generated' in response_data['messages'][0]['html']
    
    # Verify the iteration counter was incremented
    user_with_no_clubs.refresh_from_db()
    assert user_with_no_clubs.api_key_iter == 1
    # The signed token should validate correctly
    assert user_with_no_clubs.check_api_key(response_data['props']['apiKey'])


@pytest.mark.django_db
def test_generate_api_key_revokes_previous(bridge_client: Client, user_with_no_clubs):
    """Test that generating a new API key revokes the previous one"""
    bridge_client.force_login(user_with_no_clubs)
    
    # Generate first API key
    response1 = bridge_client.post('/accounts/profile/api-key/generate/')
    first_key = response1.json()['props']['apiKey']
    
    # Generate second API key
    response2 = bridge_client.post('/accounts/profile/api-key/generate/')
    second_key = response2.json()['props']['apiKey']
    
    # Keys should be different
    assert first_key != second_key
    
    # Database should have incremented the iteration counter
    user_with_no_clubs.refresh_from_db()
    assert user_with_no_clubs.api_key_iter == 2
    # Old key should no longer work
    assert not user_with_no_clubs.check_api_key(first_key)
    # New key should work
    assert user_with_no_clubs.check_api_key(second_key)


@pytest.mark.django_db
def test_revoke_api_key(bridge_client: Client, user_with_no_clubs):
    """Test revoking an API key"""
    bridge_client.force_login(user_with_no_clubs)
    
    # First generate a key
    response = bridge_client.post('/accounts/profile/api-key/generate/')
    generated_key = response.json()['props']['apiKey']
    user_with_no_clubs.refresh_from_db()
    assert user_with_no_clubs.api_key_iter == 1
    
    # Revoke the key
    response = bridge_client.post('/accounts/profile/api-key/revoke/')
    assert response.status_code == 200
    response_data = response.json()
    
    # Check response structure
    assert response_data['props']['hasApiKey'] is False
    
    # Check success message
    assert len(response_data['messages']) == 1
    assert response_data['messages'][0]['level'] == 'success'
    assert 'API key revoked' in response_data['messages'][0]['html']
    
    # Verify the iteration counter was incremented (invalidating the old key)
    user_with_no_clubs.refresh_from_db()
    assert user_with_no_clubs.api_key_iter == 2
    # Old key should no longer work
    assert not user_with_no_clubs.check_api_key(generated_key)


@pytest.mark.django_db
def test_revoke_api_key_when_none_exists(bridge_client: Client, user_with_no_clubs):
    """Test that revoking when no key exists doesn't cause errors"""
    bridge_client.force_login(user_with_no_clubs)
    
    # Revoke without having a key
    response = bridge_client.post('/accounts/profile/api-key/revoke/')
    assert response.status_code == 200
    response_data = response.json()
    
    assert response_data['props']['hasApiKey'] is False


@pytest.mark.django_db
def test_generate_api_key_requires_login(client: Client):
    """Test that generating API key requires authentication"""
    response = client.post('/accounts/profile/api-key/generate/')
    assert response.status_code == 302
    assert '/accounts/login/' in response.url


@pytest.mark.django_db
def test_revoke_api_key_requires_login(client: Client):
    """Test that revoking API key requires authentication"""
    response = client.post('/accounts/profile/api-key/revoke/')
    assert response.status_code == 302
    assert '/accounts/login/' in response.url


# API Key Authentication Middleware Tests

@pytest.mark.django_db
def test_api_key_authentication_success(client: Client, user_with_no_clubs):
    """Test successful authentication with API key"""
    # Generate an API key for the user (returns plain text)
    api_key = user_with_no_clubs.generate_api_key()
    
    # Make a request with the API key
    response = client.get('/accounts/profile/', HTTP_AUTHORIZATION=f'Bearer {api_key}')
    
    # Should be able to access the profile page
    assert response.status_code == 200


@pytest.mark.django_db
def test_api_key_authentication_invalid_key(client: Client):
    """Test that invalid API key doesn't authenticate"""
    # Make a request with an invalid API key
    response = client.get('/accounts/profile/', HTTP_AUTHORIZATION='Bearer invalid_key_12345')
    
    # Should redirect to login since not authenticated
    assert response.status_code == 302
    assert '/accounts/login/' in response.url


@pytest.mark.django_db
def test_api_key_authentication_no_bearer_prefix(client: Client, user_with_no_clubs):
    """Test that API key without Bearer prefix doesn't work"""
    api_key = user_with_no_clubs.generate_api_key()
    
    # Try without Bearer prefix
    response = client.get('/accounts/profile/', HTTP_AUTHORIZATION=api_key)
    
    # Should not authenticate
    assert response.status_code == 302
    assert '/accounts/login/' in response.url


@pytest.mark.django_db
def test_api_key_authentication_malformed_header(client: Client):
    """Test that malformed authorization header doesn't cause errors"""
    response = client.get('/accounts/profile/', HTTP_AUTHORIZATION='NotBearer something')
    
    # Should redirect to login
    assert response.status_code == 302
    assert '/accounts/login/' in response.url


@pytest.mark.django_db
def test_api_key_authentication_with_bridge_client(bridge_client: Client, user_with_no_clubs):
    """Test API key authentication works with bridge client"""
    api_key = user_with_no_clubs.generate_api_key()
    
    response = bridge_client.get(
        '/accounts/profile/',
        HTTP_AUTHORIZATION=f'Bearer {api_key}'
    )
    
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['context']['user']['authenticated'] is True
    assert response_data['context']['user']['id'] == user_with_no_clubs.id


@pytest.mark.django_db
def test_cookie_auth_still_works(bridge_client: Client, user_with_no_clubs):
    """Test that cookie-based authentication still works alongside API key auth"""
    bridge_client.force_login(user_with_no_clubs)
    
    # Access without API key, just cookies
    response = bridge_client.get('/accounts/profile/')
    
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['context']['user']['authenticated'] is True
    assert response_data['context']['user']['id'] == user_with_no_clubs.id


@pytest.mark.django_db
def test_api_key_takes_precedence_over_cookies(bridge_client: Client, user_with_no_clubs, user_with_buncha_clubs):
    """Test that API key authentication takes precedence over cookie auth"""
    # Log in as one user via cookies
    bridge_client.force_login(user_with_no_clubs)
    
    # But use another user's API key
    api_key = user_with_buncha_clubs.generate_api_key()
    
    response = bridge_client.get(
        '/accounts/profile/',
        HTTP_AUTHORIZATION=f'Bearer {api_key}'
    )
    
    assert response.status_code == 200
    response_data = response.json()
    
    # Should be authenticated as the user whose API key was used
    assert response_data['context']['user']['authenticated'] is True
    assert response_data['context']['user']['id'] == user_with_buncha_clubs.id


@pytest.mark.django_db
def test_revoked_api_key_no_longer_works(client: Client, user_with_no_clubs):
    """Test that revoked API key can no longer authenticate"""
    # Generate and then revoke an API key
    api_key = user_with_no_clubs.generate_api_key()
    user_with_no_clubs.revoke_api_key()
    
    # Try to use the revoked key
    response = client.get('/accounts/profile/', HTTP_AUTHORIZATION=f'Bearer {api_key}')
    
    # Should not authenticate
    assert response.status_code == 302
    assert '/accounts/login/' in response.url


# User Model API Key Methods Tests

@pytest.mark.django_db
def test_user_generate_api_key_returns_key():
    """Test that generate_api_key returns the generated key"""
    user = User.objects.create_user(username="testuser")
    api_key = user.generate_api_key()
    
    assert api_key is not None
    assert len(api_key) > 0
    # The iteration counter should be incremented
    assert user.api_key_iter == 1
    # The signed token should validate correctly
    assert user.check_api_key(api_key)


@pytest.mark.django_db
def test_user_api_key_is_unique():
    """Test that generated API keys are unique (statistically)"""
    user1 = User.objects.create_user(username="user1")
    user2 = User.objects.create_user(username="user2")
    
    key1 = user1.generate_api_key()
    key2 = user2.generate_api_key()
    
    # Keys should be different
    assert key1 != key2


@pytest.mark.django_db
def test_user_revoke_api_key_sets_to_none():
    """Test that revoke_api_key increments the iteration counter"""
    user = User.objects.create_user(username="testuser")
    user.generate_api_key()
    assert user.api_key_iter == 1
    
    user.revoke_api_key()
    assert user.api_key_iter == 2


@pytest.mark.django_db
def test_user_revoke_api_key_when_none_exists():
    """Test that revoking when no key exists just increments the counter"""
    user = User.objects.create_user(username="testuser")
    assert user.api_key_iter == 0
    
    user.revoke_api_key()
    assert user.api_key_iter == 1


@pytest.mark.django_db
def test_multiple_users_can_have_api_keys():
    """Test that multiple users can each have their own API keys"""
    user1 = User.objects.create_user(username="user1")
    user2 = User.objects.create_user(username="user2")
    
    key1 = user1.generate_api_key()
    key2 = user2.generate_api_key()
    
    # Both should have incremented iteration counters
    assert user1.api_key_iter == 1
    assert user2.api_key_iter == 1
    
    # Keys should be different (different user IDs in the signed data)
    assert key1 != key2
    
    # Each user should validate their own key
    assert user1.check_api_key(key1)
    assert user2.check_api_key(key2)
    # But not the other's key
    assert not user1.check_api_key(key2)
    assert not user2.check_api_key(key1)


@pytest.mark.django_db
def test_api_key_format_includes_user_id():
    """Test that API keys can be unsigned to reveal user ID and iteration"""
    from django.core.signing import Signer
    
    user = User.objects.create_user(username="testuser")
    api_key = user.generate_api_key()
    
    # Should be able to unsign the key
    signer = Signer()
    unsigned_value = signer.unsign_object(api_key)
    
    # Should contain user_id and iter as a dict
    assert isinstance(unsigned_value, dict)
    assert unsigned_value["user_id"] == user.id
    assert unsigned_value["iter"] == 1  # First iteration


@pytest.mark.django_db
def test_get_user_from_api_key_efficient_lookup():
    """Test that get_user_from_api_key can efficiently look up the user"""
    user1 = User.objects.create_user(username="user1")
    user2 = User.objects.create_user(username="user2")
    
    key1 = user1.generate_api_key()
    key2 = user2.generate_api_key()
    
    # Should be able to get the correct user from the key
    assert User.get_user_from_api_key(key1) == user1
    assert User.get_user_from_api_key(key2) == user2
    
    # Invalid keys should return None
    assert User.get_user_from_api_key("invalid_key") is None
    assert User.get_user_from_api_key("totally:bogus:data") is None


@pytest.mark.django_db
def test_api_key_with_tampered_signature_rejected():
    """Test that keys with invalid signatures are rejected"""
    user = User.objects.create_user(username="testuser")
    api_key = user.generate_api_key()
    
    # Tamper with the signature
    tampered_key = api_key[:-5] + "XXXXX"
    
    result = User.get_user_from_api_key(tampered_key)
    assert result is None
    assert not user.check_api_key(tampered_key)


@pytest.mark.django_db
def test_api_key_with_old_iteration_rejected():
    """Test that keys with old iteration numbers are rejected"""
    from django.core.signing import Signer
    
    user = User.objects.create_user(username="testuser")
    
    # Generate a key with iteration 1
    old_key = user.generate_api_key()
    assert user.api_key_iter == 1
    
    # Increment to iteration 2
    user.generate_api_key()
    assert user.api_key_iter == 2
    
    # Old key should no longer work
    assert not user.check_api_key(old_key)
    assert User.get_user_from_api_key(old_key) is None
