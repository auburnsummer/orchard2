
import pytest
from django.utils import timezone
from datetime import timedelta
from freezegun import freeze_time

from cafe.models.clubs.club import Club
from cafe.models.clubs.club_membership import ClubMembership
from cafe.models.clubs.club_invite import ClubInvite


@pytest.mark.django_db
def test_get_redeem_invite_returns_no_invite_if_invite_does_not_exist(bridge_client, user_with_no_clubs):
    bridge_client.force_login(user_with_no_clubs)
    response = bridge_client.get('/groups/redeem_invite/nonexistent_code/')
    
    assert response.status_code == 200
    body = response.json()
    assert body['props']['invite'] is None
    assert body['props']['code'] == 'nonexistent_code'
    assert body['props']['membership'] is None


@pytest.mark.django_db
def test_get_redeem_invite_returns_no_invite_if_invite_expired(bridge_client, user_with_no_clubs, expired_invite):
    bridge_client.force_login(user_with_no_clubs)
    
    # Test the invite after it has expired
    with freeze_time("2023-01-02"):
        response = bridge_client.get(f'/groups/redeem_invite/{expired_invite.code}/')
    
    assert response.status_code == 200
    body = response.json()
    assert body['props']['invite'] is None
    assert body['props']['code'] == expired_invite.code
    assert body['props']['membership'] is None


@pytest.mark.django_db
def test_get_redeem_invite_sends_current_role_if_user_has_one(bridge_client, user_with_buncha_clubs):
    bridge_client.force_login(user_with_buncha_clubs)
    
    # Create an invite for a club the user is already a member of
    club = Club.objects.get(id="ca")  # user_with_buncha_clubs is owner of this club
    invite = ClubInvite.objects.create(
        club=club,
        role="admin",
        expiry=timezone.now() + timedelta(hours=24),
        code="test_code"
    )
    
    response = bridge_client.get('/groups/redeem_invite/test_code/')
    
    assert response.status_code == 200
    body = response.json()
    assert body['props']['invite'] is not None
    assert body['props']['invite']['club']['id'] == 'ca'
    assert body['props']['membership'] is not None
    assert body['props']['membership']['role'] == 'owner'


@pytest.mark.django_db
def test_post_redeem_invite_returns_404_if_invite_does_not_exist(bridge_client, user_with_no_clubs):
    bridge_client.force_login(user_with_no_clubs)
    response = bridge_client.post('/groups/redeem_invite/nonexistent_code/')
    
    assert response.status_code == 404


@pytest.mark.django_db
def test_post_redeem_invite_returns_403_if_invite_expired(bridge_client, user_with_no_clubs, expired_invite):
    bridge_client.force_login(user_with_no_clubs)
    
    # Try to redeem the invite after it has expired
    with freeze_time("2023-01-02"):
        response = bridge_client.post(f'/groups/redeem_invite/{expired_invite.code}/')
    
    assert response.status_code == 403


@pytest.mark.django_db
def test_post_redeem_invite_adds_user_to_club_if_not_in_club(bridge_client, user_with_no_clubs, valid_invite):
    bridge_client.force_login(user_with_no_clubs)
    
    # Verify user is not in club initially
    assert not ClubMembership.objects.filter(user=user_with_no_clubs, club=valid_invite.club).exists()
    
    response = bridge_client.post(f'/groups/redeem_invite/{valid_invite.code}/')
    
    # Bridge client intercepts redirects and returns 200 with redirect info
    assert response.status_code == 200
    body = response.json()
    assert body['action'] == 'redirect'
    assert f'/groups/{valid_invite.club.id}/settings/members/' in body['path']
    
    # Verify user was added to club
    membership = ClubMembership.objects.get(user=user_with_no_clubs, club=valid_invite.club)
    assert membership.role == "admin"


@pytest.mark.django_db
def test_post_redeem_invite_deletes_invite_after_redemption(bridge_client, user_with_no_clubs, valid_invite):
    bridge_client.force_login(user_with_no_clubs)
    
    # Verify invite exists
    assert ClubInvite.objects.filter(code=valid_invite.code).exists()
    
    response = bridge_client.post(f'/groups/redeem_invite/{valid_invite.code}/')
    
    assert response.status_code == 200
    
    # Verify invite was deleted
    assert not ClubInvite.objects.filter(code=valid_invite.code).exists()


@pytest.mark.django_db
def test_post_redeem_invite_sets_user_role_if_already_in_club(bridge_client, user_with_admin_membership, test_club):
    bridge_client.force_login(user_with_admin_membership)
    
    # Create invite for same role (admin)
    invite = ClubInvite.objects.create(
        club=test_club,
        role="admin", 
        expiry=timezone.now() + timedelta(hours=24),
        code="same_role_code"
    )
    
    response = bridge_client.post('/groups/redeem_invite/same_role_code/')
    
    assert response.status_code == 200
    
    # Verify role stayed the same
    membership = ClubMembership.objects.get(user=user_with_admin_membership, club=test_club)
    assert membership.role == "admin"
    
    # Verify invite was NOT deleted since no meaningful upgrade occurred
    assert ClubInvite.objects.filter(code="same_role_code").exists()


@pytest.mark.django_db
def test_post_redeem_invite_does_not_downgrade_user_from_owner(bridge_client, user_with_buncha_clubs):
    bridge_client.force_login(user_with_buncha_clubs)
    
    # user_with_buncha_clubs is owner of club "ca", try to "downgrade" them to admin
    club = Club.objects.get(id="ca")
    invite = ClubInvite.objects.create(
        club=club,
        role="admin",
        expiry=timezone.now() + timedelta(hours=24),
        code="downgrade_code"
    )
    
    # Verify current role
    membership = ClubMembership.objects.get(user=user_with_buncha_clubs, club=club)
    assert membership.role == "owner"
    
    response = bridge_client.post('/groups/redeem_invite/downgrade_code/')
    
    assert response.status_code == 200
    
    # Verify role was NOT changed (still owner)
    membership.refresh_from_db()
    assert membership.role == "owner"
    
    # Verify invite was NOT deleted since no new membership was created
    assert ClubInvite.objects.filter(code="downgrade_code").exists()


@pytest.mark.django_db
def test_post_redeem_invite_deletes_invite_when_upgrading_to_owner(bridge_client, user_with_buncha_clubs, owner_invite):
    bridge_client.force_login(user_with_buncha_clubs)
    
    # user_with_buncha_clubs is admin of club "cb", we'll use the owner_invite for a different club
    # Let's modify the invite to use club "cb" 
    club = Club.objects.get(id="cb")
    owner_invite.club = club
    owner_invite.save()
    
    # Verify current role and invite exists
    membership = ClubMembership.objects.get(user=user_with_buncha_clubs, club=club)
    assert membership.role == "admin"
    assert ClubInvite.objects.filter(code=owner_invite.code).exists()
    
    response = bridge_client.post(f'/groups/redeem_invite/{owner_invite.code}/')
    
    assert response.status_code == 200
    
    # Verify role was updated to owner
    membership.refresh_from_db()
    assert membership.role == "owner"
    
    # Verify invite was deleted when upgrading to owner
    assert not ClubInvite.objects.filter(code=owner_invite.code).exists()