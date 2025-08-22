
import pytest
from django.contrib.auth.models import AnonymousUser


@pytest.mark.django_db
def test_anonymous_user_cannot_change_rdlevel(rdlevel):
    """Anonymous users should not have permission to change RDLevels"""
    anonymous_user = AnonymousUser()
    assert not anonymous_user.has_perm('cafe.change_rdlevel', rdlevel)


@pytest.mark.django_db
def test_non_submitter_cannot_change_rdlevel(rdlevel):
    """Users who are not the submitter and not admin of the connected club should not have permission"""
    from cafe.models.user import User
    
    other_user = User.objects.create_user(username="other_user", display_name="Other User")
    assert not other_user.has_perm('cafe.change_rdlevel', rdlevel)


@pytest.mark.django_db
def test_submitter_can_change_rdlevel(rdlevel):
    """The submitter of an RDLevel should have permission to change it"""
    submitter = rdlevel.submitter
    assert submitter.has_perm('cafe.change_rdlevel', rdlevel)


@pytest.mark.django_db
def test_admin_of_connected_club_can_change_rdlevel(rdlevel, user_with_admin_membership):
    """Admins of the club that owns the RDLevel should have permission to change it"""
    admin_user = user_with_admin_membership
    assert admin_user.has_perm('cafe.change_rdlevel', rdlevel)


@pytest.mark.django_db
def test_superuser_can_change_rdlevel(rdlevel):
    """Superusers should have permission to change any RDLevel"""
    from cafe.models.user import User
    
    superuser = User.objects.create_superuser(
        username="superuser", 
        password="testpass",
        display_name="Super User"
    )
    assert superuser.has_perm('cafe.change_rdlevel', rdlevel)


@pytest.mark.django_db
def test_admin_of_different_club_cannot_change_rdlevel(rdlevel):
    """Admins of a different club should not have permission to change the RDLevel"""
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
    
    # Should not have permission for rdlevel from a different club
    assert not admin_user.has_perm('cafe.change_rdlevel', rdlevel)


@pytest.mark.django_db
def test_delete_permissions_same_as_change_permissions(rdlevel):
    """Delete permissions should work the same as change permissions"""
    # Test with submitter
    submitter = rdlevel.submitter
    assert submitter.has_perm('cafe.delete_rdlevel', rdlevel)
    
    # Test with anonymous user
    from django.contrib.auth.models import AnonymousUser
    anonymous_user = AnonymousUser()
    assert not anonymous_user.has_perm('cafe.delete_rdlevel', rdlevel)

