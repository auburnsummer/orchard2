"""
Tests for the `prefill_code.ok` permission.

This permission controls who can access the level prefill portal with a given prefill code.
The permission is granted if one of these conditions is met:

1. The user is linked to the Discord account that originally posted the level message
    - i.e. the person using the code is the person who posted the level.
2. The user is an admin or owner of the club associated with the prefill code
    - this is the delegated level scenario. the discord server decides if the delegated
      scenario is available by allowing or disallowing the associated discord command.

The prefill code is a signed object containing:
- level_url: URL to the .rdzip file
- discord_user_id: Discord user ID of the original poster
- discord_user_name_hint: Display name hint for the Discord user
- club_id: ID of the club where the level should be submitted
"""

import pytest
from django.contrib.auth.models import AnonymousUser
from django.core.signing import BadSignature
from django.utils import timezone
from datetime import timedelta
from freezegun import freeze_time
from unittest.mock import patch

from cafe.views.discord_bot.handlers.add import addlevel_signer
from cafe.views.rdlevels.prefill.predicates import check_if_ok_to_continue
from allauth.socialaccount.models import SocialAccount


@pytest.fixture
def valid_prefill_payload(test_club):
    """Create a valid payload for prefill code testing"""
    return {
        "level_url": "https://example.com/test.rdzip",
        "discord_user_id": "123456789",
        "discord_user_name_hint": "TestUser",
        "club_id": test_club.id
    }


@pytest.fixture
def valid_signed_code(valid_prefill_payload):
    """Create a valid signed prefill code"""
    return addlevel_signer.sign_object(valid_prefill_payload)


@pytest.fixture
def user_with_discord_account():
    """Create a user with a linked Discord social account"""
    from cafe.models.user import User
    
    user = User.objects.create_user(username="discord_user", display_name="Discord User")
    SocialAccount.objects.create(
        user=user,
        provider='discord',
        uid='123456789',  # This matches the discord_user_id in valid_prefill_payload
        extra_data={}
    )
    return user


@pytest.fixture
def user_without_discord_account():
    """Create a user without a Discord social account"""
    from cafe.models.user import User
    return User.objects.create_user(username="no_discord", display_name="No Discord")


@pytest.fixture
def user_with_different_discord_account():
    """Create a user with a different Discord social account"""
    from cafe.models.user import User
    
    user = User.objects.create_user(username="other_discord", display_name="Other Discord")
    SocialAccount.objects.create(
        user=user,
        provider='discord',
        uid='987654321',  # Different from the one in valid_prefill_payload
        extra_data={}
    )
    return user


@pytest.mark.django_db
def test_check_if_ok_to_continue_with_valid_code_and_matching_discord_account(
    user_with_discord_account, valid_signed_code
):
    """User with matching Discord account should be allowed to continue"""
    result = check_if_ok_to_continue(user_with_discord_account, valid_signed_code)
    assert result is True


@pytest.mark.django_db
def test_check_if_ok_to_continue_with_invalid_signature(user_with_discord_account):
    """Invalid signature should not be allowed"""
    invalid_code = "invalid.signature.here"
    result = check_if_ok_to_continue(user_with_discord_account, invalid_code)
    assert result is False


@pytest.mark.django_db
def test_check_if_ok_to_continue_with_expired_code(user_with_discord_account, valid_prefill_payload):
    """Expired code should not be allowed"""
    # Create a code that was signed 2 days ago (beyond the 1 day limit)
    with freeze_time("2023-01-01"):
        expired_code = addlevel_signer.sign_object(valid_prefill_payload)
    
    # Now try to use it 2 days later
    with freeze_time("2023-01-03"):
        result = check_if_ok_to_continue(user_with_discord_account, expired_code)
        assert result is False


@pytest.mark.django_db
def test_check_if_ok_to_continue_with_nonexistent_club(user_with_discord_account):
    """Code referencing nonexistent club should not be allowed"""
    payload_with_bad_club = {
        "level_url": "https://example.com/test.rdzip",
        "discord_user_id": "123456789",
        "discord_user_name_hint": "TestUser",
        "club_id": "nonexistent_club_id"
    }
    bad_code = addlevel_signer.sign_object(payload_with_bad_club)
    result = check_if_ok_to_continue(user_with_discord_account, bad_code)
    assert result is False


@pytest.mark.django_db
def test_check_if_ok_to_continue_with_no_matching_discord_account_and_no_club_permissions(
    user_without_discord_account, valid_signed_code
):
    """User without matching Discord account and no club permissions should not be allowed"""
    result = check_if_ok_to_continue(user_without_discord_account, valid_signed_code)
    assert result is False


@pytest.mark.django_db
def test_check_if_ok_to_continue_with_different_discord_account_and_no_club_permissions(
    user_with_different_discord_account, valid_signed_code
):
    """User with different Discord account and no club permissions should not be allowed"""
    result = check_if_ok_to_continue(user_with_different_discord_account, valid_signed_code)
    assert result is False


@pytest.mark.django_db
def test_check_if_ok_to_continue_with_club_admin_permissions(
    test_club, user_without_discord_account, valid_signed_code
):
    """User with admin permissions on the club should be allowed, even without matching Discord account"""
    from cafe.models.clubs.club_membership import ClubMembership
    
    # Make the user an admin of the club
    ClubMembership.objects.create(
        user=user_without_discord_account,
        club=test_club,
        role="admin"
    )
    
    result = check_if_ok_to_continue(user_without_discord_account, valid_signed_code)
    assert result is True


@pytest.mark.django_db
def test_check_if_ok_to_continue_with_club_owner_permissions(
    test_club, user_without_discord_account, valid_signed_code
):
    """User with owner permissions on the club should be allowed, even without matching Discord account"""
    from cafe.models.clubs.club_membership import ClubMembership
    
    # Make the user an owner of the club
    ClubMembership.objects.create(
        user=user_without_discord_account,
        club=test_club,
        role="owner"
    )
    
    result = check_if_ok_to_continue(user_without_discord_account, valid_signed_code)
    assert result is True


@pytest.mark.django_db
def test_check_if_ok_to_continue_with_club_member_permissions(
    test_club, user_without_discord_account, valid_signed_code
):
    """User with only member permissions on the club should not be allowed"""
    from cafe.models.clubs.club_membership import ClubMembership
    
    # Make the user a regular member of the club (not admin/owner)
    ClubMembership.objects.create(
        user=user_without_discord_account,
        club=test_club,
        role="member"
    )
    
    result = check_if_ok_to_continue(user_without_discord_account, valid_signed_code)
    assert result is False


@pytest.mark.django_db
def test_check_if_ok_to_continue_with_anonymous_user(valid_signed_code):
    """Anonymous users should not be allowed"""
    anonymous_user = AnonymousUser()
    result = check_if_ok_to_continue(anonymous_user, valid_signed_code)
    assert result is False


@pytest.mark.django_db
def test_check_if_ok_to_continue_with_discord_account_and_club_permissions(
    test_club, user_with_discord_account, valid_signed_code
):
    """User with both matching Discord account AND club permissions should be allowed"""
    from cafe.models.clubs.club_membership import ClubMembership
    
    # Make the user an admin of the club as well
    ClubMembership.objects.create(
        user=user_with_discord_account,
        club=test_club,
        role="admin"
    )
    
    result = check_if_ok_to_continue(user_with_discord_account, valid_signed_code)
    assert result is True


@pytest.mark.django_db
def test_permission_rules_integration():
    """Test that the permission is properly registered with django-rules"""
    import rules
    from cafe.views.rdlevels.prefill.predicates import register_permissions
    
    # Register the permissions (normally done on module import)
    register_permissions()
    
    # The permission should be registered
    assert rules.perm_exists('prefill_code.ok')
    
    # Test with dummy data to ensure the predicate is callable
    from cafe.models.user import User
    user = User.objects.create_user(username="test", display_name="Test")
    
    # This should not crash (actual permission testing is done in other tests)
    has_perm = user.has_perm('prefill_code.ok', 'dummy_code')
    # We expect False since 'dummy_code' is not a valid signed code
    assert has_perm is False


@pytest.mark.django_db
def test_malformed_json_in_signed_code(user_with_discord_account):
    """Test handling of code that can be unsigned but contains malformed data"""
    # Create a code with invalid structure (missing required keys)
    malformed_payload = {"invalid": "structure"}
    malformed_code = addlevel_signer.sign_object(malformed_payload)
    
    # This should handle the KeyError gracefully and return False
    result = check_if_ok_to_continue(user_with_discord_account, malformed_code)
    assert result is False


@pytest.mark.django_db 
def test_multiple_discord_accounts_same_user(test_club, valid_prefill_payload):
    """Test user with multiple Discord social accounts"""
    from cafe.models.user import User
    
    user = User.objects.create_user(username="multi_discord", display_name="Multi Discord")
    
    # Create multiple Discord social accounts for the same user
    SocialAccount.objects.create(
        user=user,
        provider='discord',
        uid='111111111',
        extra_data={}
    )
    SocialAccount.objects.create(
        user=user,
        provider='discord', 
        uid='123456789',  # This matches our test payload
        extra_data={}
    )
    
    valid_signed_code = addlevel_signer.sign_object(valid_prefill_payload)
    result = check_if_ok_to_continue(user, valid_signed_code)
    assert result is True


@pytest.mark.django_db
def test_non_discord_social_account(user_without_discord_account, valid_signed_code):
    """Test user with social account from different provider"""
    # Add a non-Discord social account
    SocialAccount.objects.create(
        user=user_without_discord_account,
        provider='github',  # Different provider
        uid='123456789',    # Same UID but different provider
        extra_data={}
    )
    
    result = check_if_ok_to_continue(user_without_discord_account, valid_signed_code)
    assert result is False


@pytest.mark.django_db
def test_edge_case_string_vs_int_discord_id(test_club):
    """Test handling of Discord ID as string vs int"""
    from cafe.models.user import User
    
    user = User.objects.create_user(username="string_id", display_name="String ID")
    
    # Create social account with string UID
    SocialAccount.objects.create(
        user=user,
        provider='discord',
        uid='123456789',  # String UID
        extra_data={}
    )
    
    # Create payload with int discord_user_id
    payload_with_int_id = {
        "level_url": "https://example.com/test.rdzip",
        "discord_user_id": 123456789,  # Int instead of string
        "discord_user_name_hint": "TestUser",
        "club_id": test_club.id
    }
    
    signed_code = addlevel_signer.sign_object(payload_with_int_id)
    result = check_if_ok_to_continue(user, signed_code)
    
    # Should still work due to Django's flexible matching
    assert result is True
