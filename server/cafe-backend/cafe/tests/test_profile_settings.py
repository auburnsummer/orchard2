from django.test import Client
import pytest

def test_profile_clubs_does_not_allow_anonymous(client: Client):
    response = client.get('/accounts/profile/settings/')
    assert response.status_code == 302
    assert response.url == '/accounts/login/?next=/accounts/profile/settings/'

@pytest.mark.django_db
def test_profile_settings_can_change_settings(bridge_client: Client, user_with_no_clubs):
    bridge_client.force_login(user_with_no_clubs)
    response = bridge_client.get('/accounts/profile/settings/')
    assert response.status_code == 200
    assert response.json()['context']['user']['theme_preference'] == 'light'
    assert response.json()['context']['user']['displayName'] == ''
    # Now, let's change the settings
    response = bridge_client.post('/accounts/profile/settings/', {
        'theme_preference': 'dark',
        'display_name': 'Test User'
    })
    assert response.status_code == 200
    assert response.json()['context']['user']['theme_preference'] == 'dark'
    assert response.json()['context']['user']['displayName'] == 'Test User'
    # and then if we fetch the settings again, they should be updated
    response = bridge_client.get('/accounts/profile/settings/')
    assert response.status_code == 200
    assert response.json()['context']['user']['theme_preference'] == 'dark'
    assert response.json()['context']['user']['displayName'] == 'Test User'

@pytest.mark.django_db
def test_profile_settings_rejects_invalid_data(bridge_client: Client, user_with_no_clubs):
    """
    If the user attempts to submit a form with a theme_preference that is not valid,
    i.e. not "light" or "dark", the form should not be valid and the user should not be updated.
    """
    bridge_client.force_login(user_with_no_clubs)
    
    # First, get the initial state
    response = bridge_client.get('/accounts/profile/settings/')
    assert response.status_code == 200
    initial_theme = response.json()['context']['user']['theme_preference']
    initial_display_name = response.json()['context']['user']['displayName']
    
    # Try to submit invalid theme_preference
    response = bridge_client.post('/accounts/profile/settings/', {
        'theme_preference': 'invalid_theme',
        'display_name': 'Updated Name'
    })
    
    # The response should still be 200 (the view doesn't return errors, since 
    # invalid form data _should_ be handled by the frontend but the backend
    # still needs to handle it gracefully enough to not crash etc)
    assert response.status_code == 200
    
    # Verify the user settings were NOT updated due to form validation failure
    response = bridge_client.get('/accounts/profile/settings/')
    assert response.status_code == 200
    assert response.json()['context']['user']['theme_preference'] == initial_theme
    assert response.json()['context']['user']['displayName'] == initial_display_name
    
    # Also test with another invalid theme value
    response = bridge_client.post('/accounts/profile/settings/', {
        'theme_preference': 'rainbow',
        'display_name': 'Another Name'
    })
    
    # Verify again that settings were not updated
    response = bridge_client.get('/accounts/profile/settings/')
    assert response.status_code == 200
    assert response.json()['context']['user']['theme_preference'] == initial_theme
    assert response.json()['context']['user']['displayName'] == initial_display_name


@pytest.mark.django_db
def test_profile_settings_partial_update_theme_only(bridge_client: Client, user_with_no_clubs):
    """Test updating only the theme preference while providing all required fields"""
    bridge_client.force_login(user_with_no_clubs)
    
    # Set initial state
    response = bridge_client.post('/accounts/profile/settings/', {
        'theme_preference': 'light',
        'display_name': 'Initial Name'
    })
    assert response.status_code == 200
    
    # Update theme preference while explicitly providing display_name
    response = bridge_client.post('/accounts/profile/settings/', {
        'theme_preference': 'dark',
        'display_name': 'Initial Name'  # Must provide to preserve
    })
    assert response.status_code == 200
    
    # Verify theme was updated and display name was preserved
    response = bridge_client.get('/accounts/profile/settings/')
    assert response.status_code == 200
    assert response.json()['context']['user']['theme_preference'] == 'dark'
    assert response.json()['context']['user']['displayName'] == 'Initial Name'


@pytest.mark.django_db
def test_profile_settings_partial_update_display_name_only(bridge_client: Client, user_with_no_clubs):
    """Test updating only the display name while providing all required fields"""
    bridge_client.force_login(user_with_no_clubs)
    
    # Set initial state
    response = bridge_client.post('/accounts/profile/settings/', {
        'theme_preference': 'dark',
        'display_name': 'Initial Name'
    })
    assert response.status_code == 200
    
    # Update display name while explicitly providing theme_preference
    response = bridge_client.post('/accounts/profile/settings/', {
        'theme_preference': 'dark',  # Must provide to preserve
        'display_name': 'Updated Name'
    })
    assert response.status_code == 200
    
    # Verify display name was updated and theme was preserved
    response = bridge_client.get('/accounts/profile/settings/')
    assert response.status_code == 200
    assert response.json()['context']['user']['theme_preference'] == 'dark'
    assert response.json()['context']['user']['displayName'] == 'Updated Name'


@pytest.mark.django_db
def test_profile_settings_missing_fields_resets_to_defaults(bridge_client: Client, user_with_no_clubs):
    """Test that missing fields in POST data reset to model defaults/empty values"""
    bridge_client.force_login(user_with_no_clubs)
    
    # Set initial state
    response = bridge_client.post('/accounts/profile/settings/', {
        'theme_preference': 'dark',
        'display_name': 'Test User'
    })
    assert response.status_code == 200
    
    # Submit form with only theme_preference (missing display_name)
    response = bridge_client.post('/accounts/profile/settings/', {
        'theme_preference': 'light'
        # display_name is missing, so it should reset to empty
    })
    assert response.status_code == 200
    
    # Verify display name was reset to empty string
    response = bridge_client.get('/accounts/profile/settings/')
    assert response.status_code == 200
    assert response.json()['context']['user']['theme_preference'] == 'light'
    assert response.json()['context']['user']['displayName'] == ''


@pytest.mark.django_db
def test_profile_settings_empty_display_name(bridge_client: Client, user_with_no_clubs):
    """Test that empty display name is allowed"""
    bridge_client.force_login(user_with_no_clubs)
    
    response = bridge_client.post('/accounts/profile/settings/', {
        'theme_preference': 'dark',
        'display_name': ''  # Empty string
    })
    assert response.status_code == 200
    
    # Verify empty display name was saved
    response = bridge_client.get('/accounts/profile/settings/')
    assert response.status_code == 200
    assert response.json()['context']['user']['theme_preference'] == 'dark'
    assert response.json()['context']['user']['displayName'] == ''


@pytest.mark.django_db
def test_profile_settings_success_message(bridge_client: Client, user_with_no_clubs):
    """Test that success message is added when form is valid"""
    bridge_client.force_login(user_with_no_clubs)
    
    response = bridge_client.post('/accounts/profile/settings/', {
        'theme_preference': 'dark',
        'display_name': 'Test User'
    })
    assert response.status_code == 200
    
    # Check that the response contains the expected structure
    response_data = response.json()
    assert response_data['action'] == 'render'
    assert response_data['view'] == 'cafe:profile_settings'
    
    # Check that the user was updated in the context
    assert response_data['context']['user']['theme_preference'] == 'dark'
    assert response_data['context']['user']['displayName'] == 'Test User'
    
    # Check that a success message was added
    assert 'messages' in response_data
    assert len(response_data['messages']) == 1
    assert response_data['messages'][0]['level'] == 'success'
    assert response_data['messages'][0]['html'] == 'User updated!'


@pytest.mark.django_db
def test_profile_settings_very_long_display_name(bridge_client: Client, user_with_no_clubs):
    """Test behavior with display name exceeding max length"""
    bridge_client.force_login(user_with_no_clubs)
    
    # Create a display name longer than 150 characters
    long_name = 'a' * 151
    
    response = bridge_client.post('/accounts/profile/settings/', {
        'theme_preference': 'dark',
        'display_name': long_name
    })
    assert response.status_code == 200
    
    # Verify the settings were NOT updated due to validation failure
    response = bridge_client.get('/accounts/profile/settings/')
    assert response.status_code == 200
    # Should still have default values since form was invalid
    assert response.json()['context']['user']['displayName'] == ''
