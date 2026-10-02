
import pytest
from django.contrib.auth.models import AnonymousUser


@pytest.fixture
def pharmacy_club():
    """Create the pharmacy club (cpharmacy)"""
    from cafe.models.clubs.club import Club
    return Club.objects.create(id="cpharmacy", name="Pharmacy")


@pytest.fixture
def pharmacist_user(pharmacy_club):
    """Create a user who is an admin of the pharmacy club (a pharmacist)"""
    from cafe.models.user import User
    from cafe.models.clubs.club_membership import ClubMembership
    
    user = User.objects.create_user(username="pharmacist_user", display_name="Pharmacist User")
    ClubMembership.objects.create(
        user=user,
        club=pharmacy_club,
        role="admin"
    )
    return user


@pytest.fixture
def pharmacist_owner(pharmacy_club):
    """Create a user who is an owner of the pharmacy club (also a pharmacist)"""
    from cafe.models.user import User
    from cafe.models.clubs.club_membership import ClubMembership
    
    user = User.objects.create_user(username="pharmacist_owner", display_name="Pharmacist Owner")
    ClubMembership.objects.create(
        user=user,
        club=pharmacy_club,
        role="owner"
    )
    return user


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
def test_non_pharmacist_delete_permissions_match_change_permissions(rdlevel):
    """For non-pharmacists, delete permissions should match change permissions (submitter can delete)"""
    # Test with submitter
    submitter = rdlevel.submitter
    assert submitter.has_perm('cafe.delete_rdlevel', rdlevel)
    
    # Test with anonymous user
    from django.contrib.auth.models import AnonymousUser
    anonymous_user = AnonymousUser()
    assert not anonymous_user.has_perm('cafe.delete_rdlevel', rdlevel)


# Pharmacist Permission Tests

@pytest.mark.django_db
def test_pharmacist_can_change_any_rdlevel(rdlevel, pharmacist_user):
    """Pharmacists (admins/owners of cpharmacy) can change any RDLevel regardless of club or submitter"""
    assert pharmacist_user.has_perm('cafe.change_rdlevel', rdlevel)


@pytest.mark.django_db
def test_pharmacist_owner_can_change_any_rdlevel(rdlevel, pharmacist_owner):
    """Pharmacist owners can also change any RDLevel"""
    assert pharmacist_owner.has_perm('cafe.change_rdlevel', rdlevel)


@pytest.mark.django_db
def test_pharmacist_can_delete_rdlevel(rdlevel, pharmacist_user):
    """Pharmacists can delete RDLevels"""
    assert pharmacist_user.has_perm('cafe.delete_rdlevel', rdlevel)


@pytest.mark.django_db
def test_pharmacist_owner_can_delete_rdlevel(rdlevel, pharmacist_owner):
    """Pharmacist owners can also delete RDLevels"""
    assert pharmacist_owner.has_perm('cafe.delete_rdlevel', rdlevel)


@pytest.mark.django_db
def test_pharmacist_can_change_level_from_different_club(rdlevel, pharmacist_user):
    """Pharmacists can edit levels from clubs they're not members of"""
    # Verify pharmacist is not a member of the rdlevel's club
    from cafe.models.clubs.club_membership import ClubMembership
    memberships = ClubMembership.objects.filter(user=pharmacist_user, club=rdlevel.club)
    assert len(memberships) == 0
    
    # But they can still change the level
    assert pharmacist_user.has_perm('cafe.change_rdlevel', rdlevel)


@pytest.mark.django_db
def test_non_superuser_has_no_pharmacist_permissions_when_pharmacy_club_missing(rdlevel):
    """If the pharmacy club doesn't exist, non-superusers should not get pharmacist permissions"""
    from cafe.models.user import User
    from cafe.models.clubs.club import Club
    from cafe.models.clubs.club_membership import ClubMembership
    
    # Ensure pharmacy club doesn't exist
    Club.objects.filter(id="cpharmacy").delete()
    
    # Create a regular user who would be a pharmacist if the club existed
    user = User.objects.create_user(username="would_be_pharmacist", display_name="Would Be Pharmacist")
    
    # User should not have change permission (assuming they're not the submitter or club admin)
    assert not user.has_perm('cafe.change_rdlevel', rdlevel)
    
    # User should not have peerreview permission
    assert not user.has_perm('cafe.peerreview_rdlevel', rdlevel)


# Peer Review Permission Tests

@pytest.mark.django_db
def test_pharmacist_can_peerreview(rdlevel, pharmacist_user):
    """Pharmacists can perform peer review"""
    assert pharmacist_user.has_perm('cafe.peerreview_rdlevel', rdlevel)


@pytest.mark.django_db
def test_pharmacist_owner_can_peerreview(rdlevel, pharmacist_owner):
    """Pharmacist owners can also perform peer review"""
    assert pharmacist_owner.has_perm('cafe.peerreview_rdlevel', rdlevel)


@pytest.mark.django_db
def test_superuser_can_peerreview(rdlevel):
    """Superusers can perform peer review"""
    from cafe.models.user import User
    
    superuser = User.objects.create_superuser(
        username="superuser_review",
        password="testpass",
        display_name="Super User"
    )
    assert superuser.has_perm('cafe.peerreview_rdlevel', rdlevel)


@pytest.mark.django_db
def test_submitter_cannot_peerreview(rdlevel):
    """Submitters cannot peer review their own levels"""
    submitter = rdlevel.submitter
    assert not submitter.has_perm('cafe.peerreview_rdlevel', rdlevel)


@pytest.mark.django_db
def test_club_admin_cannot_peerreview(rdlevel, user_with_admin_membership):
    """Club admins cannot perform peer review"""
    admin_user = user_with_admin_membership
    assert not admin_user.has_perm('cafe.peerreview_rdlevel', rdlevel)


@pytest.mark.django_db
def test_regular_user_cannot_peerreview(rdlevel):
    """Regular users cannot perform peer review"""
    from cafe.models.user import User
    
    regular_user = User.objects.create_user(username="regular_user", display_name="Regular User")
    assert not regular_user.has_perm('cafe.peerreview_rdlevel', rdlevel)


@pytest.mark.django_db
def test_anonymous_user_cannot_peerreview(rdlevel):
    """Anonymous users cannot perform peer review"""
    anonymous_user = AnonymousUser()
    assert not anonymous_user.has_perm('cafe.peerreview_rdlevel', rdlevel)

