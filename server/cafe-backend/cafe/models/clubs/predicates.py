from __future__ import annotations
from typing import TYPE_CHECKING

from cafe.models.predicates import not_anonymous
from orchard.settings import PHARMACY_CLUB_ID
import rules

if TYPE_CHECKING:
    from cafe.views.types import User
    from cafe.models.clubs.club import Club
    from cafe.models.clubs.club_membership import ClubMembership

def is_role_of_club(role: str):
    @rules.predicate
    def user_has_role_in_club(user: User, club: Club):
        memberships = user.memberships.filter(role__exact=role, club__exact=club)
        for membership in memberships:
            print(membership)
            if membership.role == role:
                return True
        
        return False

    return user_has_role_in_club

is_owner = not_anonymous & is_role_of_club("owner")
is_at_least_admin = not_anonymous & (is_owner | is_role_of_club("admin"))

@rules.predicate
def is_owner_of_permission_club(user: User, clubmembership: ClubMembership):
    if not not_anonymous(user):
        return False
    club = clubmembership.club
    return is_role_of_club("owner")(user, club)

@rules.predicate
def is_permission_subject(user: User, clubmembership: ClubMembership):
    if not not_anonymous(user):
        return False
    return clubmembership.user == user

@rules.predicate
def is_pharmacist(user: User):
    from cafe.models.clubs.club import Club
    print(user)
    try:
        pharmacy_club = Club.objects.get(id=PHARMACY_CLUB_ID)
    except Club.DoesNotExist:
        return False
    
    for role in ["admin", "owner"]:
        print(role)
        if is_role_of_club(role)(user, pharmacy_club):
            return True
    return False
