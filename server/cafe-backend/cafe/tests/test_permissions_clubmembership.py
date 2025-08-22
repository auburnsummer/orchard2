import pytest
from django.contrib.auth.models import AnonymousUser


@pytest.mark.django_db
def test_anonymous_user_cannot_change_clubmembership(user_with_admin_membership):
    """Anonymous users should not have permission to change ClubMemberships"""
    from cafe.models.clubs.club_membership import ClubMembership
    
    # Get the membership
    membership = user_with_admin_membership.memberships.first()
    
    anonymous_user = AnonymousUser()
    assert not anonymous_user.has_perm('cafe.change_clubmembership', membership)


@pytest.mark.django_db
def test_anonymous_user_cannot_delete_clubmembership(user_with_admin_membership):
    """Anonymous users should not have permission to delete ClubMemberships"""
    from cafe.models.clubs.club_membership import ClubMembership
    
    # Get the membership
    membership = user_with_admin_membership.memberships.first()
    
    anonymous_user = AnonymousUser()
    assert not anonymous_user.has_perm('cafe.delete_clubmembership', membership)


@pytest.mark.django_db
def test_admin_cannot_change_clubmembership(user_with_admin_membership):
    """Admins (non-owners) should not have permission to change ClubMemberships"""
    from cafe.models.clubs.club_membership import ClubMembership
    
    # Get the membership
    membership = user_with_admin_membership.memberships.first()
    admin_user = user_with_admin_membership
    
    # Admin should not be able to change memberships (only owners can)
    assert not admin_user.has_perm('cafe.change_clubmembership', membership)


@pytest.mark.django_db
def test_admin_cannot_delete_other_membership(user_with_admin_membership, test_club):
    """Admins should not have permission to delete other users' memberships"""
    from cafe.models.user import User
    from cafe.models.clubs.club_membership import ClubMembership
    
    # Create another user with membership to the same club
    other_user = User.objects.create_user(username="other_member", display_name="Other Member")
    other_membership = ClubMembership.objects.create(
        user=other_user,
        club=test_club,
        role="admin"
    )
    
    admin_user = user_with_admin_membership
    
    # Admin should not be able to delete other users' memberships
    assert not admin_user.has_perm('cafe.delete_clubmembership', other_membership)


@pytest.mark.django_db  
def test_admin_can_delete_own_membership(user_with_admin_membership):
    """Admins should have permission to delete their own membership"""
    # Get the admin's own membership
    membership = user_with_admin_membership.memberships.first()
    admin_user = user_with_admin_membership
    
    # Admin should be able to delete their own membership
    assert admin_user.has_perm('cafe.delete_clubmembership', membership)


@pytest.mark.django_db
def test_owner_can_change_any_clubmembership(test_club):
    """Owners should have permission to change any ClubMembership in their club"""
    from cafe.models.user import User
    from cafe.models.clubs.club_membership import ClubMembership
    
    # Create owner user
    owner_user = User.objects.create_user(username="owner_user", display_name="Owner User")
    owner_membership = ClubMembership.objects.create(
        user=owner_user,
        club=test_club,
        role="owner"
    )
    
    # Create another user with membership
    other_user = User.objects.create_user(username="other_user", display_name="Other User")
    other_membership = ClubMembership.objects.create(
        user=other_user,
        club=test_club,
        role="admin"
    )
    
    # Owner should be able to change any membership in their club
    assert owner_user.has_perm('cafe.change_clubmembership', other_membership)
    assert owner_user.has_perm('cafe.change_clubmembership', owner_membership)


@pytest.mark.django_db
def test_owner_can_delete_any_clubmembership(test_club):
    """Owners should have permission to delete any ClubMembership in their club"""
    from cafe.models.user import User
    from cafe.models.clubs.club_membership import ClubMembership
    
    # Create owner user
    owner_user = User.objects.create_user(username="owner_user", display_name="Owner User")
    owner_membership = ClubMembership.objects.create(
        user=owner_user,
        club=test_club,
        role="owner"
    )
    
    # Create another user with membership
    other_user = User.objects.create_user(username="other_user", display_name="Other User")
    other_membership = ClubMembership.objects.create(
        user=other_user,
        club=test_club,
        role="admin"
    )
    
    # Owner should be able to delete any membership in their club
    assert owner_user.has_perm('cafe.delete_clubmembership', other_membership)
    assert owner_user.has_perm('cafe.delete_clubmembership', owner_membership)


@pytest.mark.django_db
def test_owner_of_different_club_cannot_change_membership(test_club):
    """Owners of different clubs should not have permission to change memberships in other clubs"""
    from cafe.models.user import User
    from cafe.models.clubs.club import Club
    from cafe.models.clubs.club_membership import ClubMembership
    
    # Create a different club with its own owner
    other_club = Club.objects.create(id="otherclub", name="Other Club")
    other_owner = User.objects.create_user(username="other_owner", display_name="Other Owner")
    ClubMembership.objects.create(
        user=other_owner,
        club=other_club,
        role="owner"
    )
    
    # Create a membership in the test club
    test_user = User.objects.create_user(username="test_user", display_name="Test User")
    test_membership = ClubMembership.objects.create(
        user=test_user,
        club=test_club,
        role="admin"
    )
    
    # Owner of other club should not be able to change membership in test club
    assert not other_owner.has_perm('cafe.change_clubmembership', test_membership)
    assert not other_owner.has_perm('cafe.delete_clubmembership', test_membership)


@pytest.mark.django_db
def test_non_member_user_cannot_change_or_delete_membership(test_club):
    """Users who are not members of the club should not have any permissions on memberships"""
    from cafe.models.user import User
    from cafe.models.clubs.club_membership import ClubMembership
    
    # Create a user who is not a member of any club
    non_member = User.objects.create_user(username="non_member", display_name="Non Member")
    
    # Create a membership in the club
    member_user = User.objects.create_user(username="member_user", display_name="Member User")
    membership = ClubMembership.objects.create(
        user=member_user,
        club=test_club,
        role="admin"
    )
    
    # Non-member should not have any permissions
    assert not non_member.has_perm('cafe.change_clubmembership', membership)
    assert not non_member.has_perm('cafe.delete_clubmembership', membership)


@pytest.mark.django_db
def test_member_can_delete_own_membership_but_not_change(test_club):
    """Members should be able to delete their own membership but not change it"""
    from cafe.models.user import User
    from cafe.models.clubs.club_membership import ClubMembership
    
    # Create a member
    member_user = User.objects.create_user(username="member_user", display_name="Member User")
    membership = ClubMembership.objects.create(
        user=member_user,
        club=test_club,
        role="admin"
    )
    
    # Member should be able to delete their own membership but not change it
    assert not member_user.has_perm('cafe.change_clubmembership', membership)
    assert member_user.has_perm('cafe.delete_clubmembership', membership)


@pytest.mark.django_db
def test_superuser_can_change_and_delete_any_membership(test_club):
    """Superusers should have permission to change and delete any ClubMembership"""
    from cafe.models.user import User
    from cafe.models.clubs.club_membership import ClubMembership
    
    # Create superuser
    superuser = User.objects.create_superuser(
        username="superuser", 
        password="testpass",
        display_name="Super User"
    )
    
    # Create a membership
    member_user = User.objects.create_user(username="member_user", display_name="Member User")
    membership = ClubMembership.objects.create(
        user=member_user,
        club=test_club,
        role="admin"
    )
    
    # Superuser should have all permissions
    assert superuser.has_perm('cafe.change_clubmembership', membership)
    assert superuser.has_perm('cafe.delete_clubmembership', membership)
