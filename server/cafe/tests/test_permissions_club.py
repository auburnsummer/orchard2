import pytest
from django.contrib.auth.models import AnonymousUser


@pytest.mark.django_db
def test_anonymous_user_cannot_view_members_or_change_info(test_club):
    """Anonymous users should not have permission to view members or change club info"""
    anonymous_user = AnonymousUser()
    assert not anonymous_user.has_perm('cafe.view_member_of_club', test_club)
    assert not anonymous_user.has_perm('cafe.change_info_of_club', test_club)


@pytest.mark.django_db 
def test_non_member_cannot_view_members_or_change_info(test_club):
    """Users who are not members of the club should not have permissions"""
    from cafe.models.user import User
    
    non_member = User.objects.create_user(username="non_member", display_name="Non Member")
    assert not non_member.has_perm('cafe.view_member_of_club', test_club)
    assert not non_member.has_perm('cafe.change_info_of_club', test_club)


@pytest.mark.django_db
def test_admin_can_view_members_but_not_change_info(test_club, user_with_admin_membership):
    """Admins should be able to view members but not change club info (only owners can)"""
    admin_user = user_with_admin_membership
    
    # Admin can view members (is_at_least_admin permission)
    assert admin_user.has_perm('cafe.view_member_of_club', test_club)
    
    # Admin cannot change info (is_owner permission required)
    assert not admin_user.has_perm('cafe.change_info_of_club', test_club)


@pytest.mark.django_db
def test_owner_can_view_members_and_change_info(test_club):
    """Owners should have both view and change permissions"""
    from cafe.models.user import User
    from cafe.models.clubs.club_membership import ClubMembership
    
    # Create an owner user
    owner_user = User.objects.create_user(username="owner_user", display_name="Owner User")
    ClubMembership.objects.create(
        user=owner_user,
        club=test_club,
        role="owner"
    )
    
    # Owner can view members (is_at_least_admin includes owners)
    assert owner_user.has_perm('cafe.view_member_of_club', test_club)
    
    # Owner can change info (is_owner permission)
    assert owner_user.has_perm('cafe.change_info_of_club', test_club)


@pytest.mark.django_db
def test_admin_of_different_club_cannot_access(test_club):
    """Admins of different clubs should not have permissions for this club"""
    from cafe.models.user import User
    from cafe.models.clubs.club import Club
    from cafe.models.clubs.club_membership import ClubMembership
    
    # Create a different club
    other_club = Club.objects.create(id="otherclub", name="Other Club")
    
    # Create a user who is admin of the other club
    admin_user = User.objects.create_user(username="other_admin", display_name="Other Admin")
    ClubMembership.objects.create(
        user=admin_user,
        club=other_club,
        role="admin"
    )
    
    # Should not have permissions for test_club
    assert not admin_user.has_perm('cafe.view_member_of_club', test_club)
    assert not admin_user.has_perm('cafe.change_info_of_club', test_club)


@pytest.mark.django_db
def test_superuser_has_all_permissions(test_club):
    """Superusers should have all permissions on any club"""
    from cafe.models.user import User
    
    superuser = User.objects.create_superuser(
        username="superuser",
        password="testpass", 
        display_name="Super User"
    )
    
    assert superuser.has_perm('cafe.view_member_of_club', test_club)
    assert superuser.has_perm('cafe.change_info_of_club', test_club)


@pytest.mark.django_db
def test_other_permissions_follow_same_patterns(test_club, user_with_admin_membership):
    """Test that other permissions follow the expected patterns"""
    from cafe.models.user import User
    from cafe.models.clubs.club_membership import ClubMembership
    
    admin_user = user_with_admin_membership
    
    # Create an owner user
    owner_user = User.objects.create_user(username="owner_user2", display_name="Owner User 2") 
    ClubMembership.objects.create(
        user=owner_user,
        club=test_club,
        role="owner"
    )
    
    # Test is_at_least_admin permissions (admin and owner should both have these)
    assert admin_user.has_perm('cafe.view_info_of_club', test_club)
    assert admin_user.has_perm('cafe.create_delegated_levels_for_club', test_club)
    assert owner_user.has_perm('cafe.view_info_of_club', test_club)
    assert owner_user.has_perm('cafe.create_delegated_levels_for_club', test_club)
    
    # Test is_owner permissions (only owner should have these)
    assert not admin_user.has_perm('cafe.create_invite_for_club', test_club)
    assert owner_user.has_perm('cafe.create_invite_for_club', test_club)
