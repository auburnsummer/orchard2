from rules.contrib.models import RulesModel
import rules
from django.db import models

from .utils import create_pk_field
from cafe.libs.gen_id import IDType
from cafe.models.predicates import not_anonymous

from django.utils import timezone

def is_role_of_club(role):
    @rules.predicate
    def user_has_role_in_club(user, club):
        memberships = user.memberships.filter(role__exact=role, club__exact=club)
        for membership in memberships:
            if membership.role == role:
                return True
        
        return False

    return user_has_role_in_club

is_owner = not_anonymous & is_role_of_club("owner")
is_at_least_admin = not_anonymous & (is_owner | is_role_of_club("admin"))

class Club(RulesModel):
    """
    A Club is a group of users and levels.

    In the website we refer to these as "groups". They're called Clubs internally to avoid
    confusion with the inbuilt django groups (which we're not using atm).
    """
    id = create_pk_field(IDType.CLUB)
    name = models.CharField(max_length=100)

    members = models.ManyToManyField("cafe.User", through="cafe.ClubMembership")

    def __str__(self):
        return f"{self.name} ({self.id})"
    
    class Meta:
        rules_permissions = {
            # cafe.view_member_of_club
            "view_member_of": is_at_least_admin,
            # cafe.view_info_of_club
            "view_info_of": is_at_least_admin,  
            # cafe.change_info_of_club
            "change_info_of": is_owner,
            # cafe.create_invite_for_club
            "create_invite_for": is_owner
        }

@rules.predicate
def is_owner_of_permission_club(user, clubmembership):
    club = clubmembership.club
    return is_role_of_club("owner")(user, club)

@rules.predicate
def is_permission_subject(user, clubmembership):
    return clubmembership.user == user

class ClubMembership(RulesModel):
    """
    A User can be a member of any number of Clubs. There are two levels of membership:

    - Owner: the user can add, remove and change users in the Club. Owners can demote other Owners.
    - Admin: the user can add/edit/delete levels under the Club.
    - ~~Member: the user can add levels under the Club.~~ 
     
    nb: Member doesn't exist yet, because atm the only way you add levels into a Club is via an
    attached discord server. So anyone who is in the discord server can add levels, even without
    needing to be a Member. The Member role will allow non-discord based uploads to add levels to
    the club. Since those don't exist yet, we don't have members yet.
    """
    user = models.ForeignKey("cafe.User", on_delete=models.CASCADE, related_name="memberships")
    club = models.ForeignKey("cafe.Club", on_delete=models.CASCADE, related_name="memberships")

    role = models.CharField(choices={
        'owner': 'Owner',
        'admin': 'Admin'
    }, max_length=10)

    def __str__(self):
        return f"{self.user} -> {self.club} [{self.role}]"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'club'], name='unique_user_and_club')
        ]

        # change permission allows both upgrades and downgrades.
        # so we can't let a user change their own role (yet)
        # todo: break this into upgrade and downgrade permissions.
        rules_permissions = {
            # cafe.change_clubmembership
            "change": is_owner_of_permission_club,
            # cafe.delete_clubmembership
            "delete": is_owner_of_permission_club | is_permission_subject
        }

class ClubInvite(models.Model):
    """
    A ClubInvite allows a user to join a Club. They can only be used once; it's deleted from the db after use.
    """
    club = models.ForeignKey("cafe.Club", on_delete=models.CASCADE)
    role = models.CharField(choices={
        'owner': 'Owner',
        'admin': 'Admin'
    }, max_length=10)
    expiry = models.DateTimeField()
    code = models.CharField(max_length=100)

    def has_expired(self):
        return timezone.now() > self.expiry

    def __str__(self):
        return f"Invite to {self.club} as {self.role}, expires {self.expiry}"