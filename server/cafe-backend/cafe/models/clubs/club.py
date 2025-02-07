from __future__ import annotations
from typing import TYPE_CHECKING
from django.db import models

from rules.contrib.models import RulesModel 
from cafe.models.id_utils import generate_club_id, CLUB_ID_LENGTH

from .predicates import is_at_least_admin, is_owner

if TYPE_CHECKING:
    from .club_membership import ClubMembership
    from django.db.models.manager import RelatedManager

class Club(RulesModel):
    """
    A Club is a group of users and levels.

    In the website we refer to these as "groups". They're called Clubs internally to avoid
    confusion with the inbuilt django groups.
    """
    id = models.CharField(max_length=CLUB_ID_LENGTH, primary_key=True, default=generate_club_id)
    name = models.CharField(max_length=100)

    members = models.ManyToManyField("cafe.User", through="cafe.ClubMembership")
    # from cafe.ClubMembership
    memberships: RelatedManager[ClubMembership]

    def __str__(self):
        return f"{self.name} ({self.id})"
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }
    
    class Meta:
        rules_permissions = {
            # cafe.view_member_of_club
            "view_member_of": is_at_least_admin,
            # cafe.view_info_of_club
            "view_info_of": is_at_least_admin,  
            # cafe.change_info_of_club
            "change_info_of": is_owner,
            # cafe.create_invite_for_club
            "create_invite_for": is_owner,
            # cafe.create_delegated_levels_for_club
            "create_delegated_levels_for": is_at_least_admin,
        }