from __future__ import annotations
from typing import TYPE_CHECKING
from django.db import models

import rules
from cafe.models.id_utils import generate_club_id, CLUB_ID_LENGTH
from simple_history.models import HistoricalRecords

from .predicates import is_at_least_admin, is_owner

if TYPE_CHECKING:
    from .club_membership import ClubMembership
    from django.db.models.manager import RelatedManager

class Club(models.Model):
    """
    A Club is a group of users and levels.

    In the website we refer to these as "groups". They're called Clubs internally to avoid
    confusion with the inbuilt django groups.
    """
    id = models.CharField(max_length=20, primary_key=True, default=generate_club_id)
    name = models.CharField(max_length=100)

    members = models.ManyToManyField("cafe.User", through="cafe.ClubMembership")
    # from cafe.ClubMembership
    memberships: RelatedManager[ClubMembership]

    history = HistoricalRecords(cascade_delete_history=True)

    def __str__(self):
        return f"{self.name} ({self.id})"
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }

rules.add_perm("cafe.view_member_of_club", is_at_least_admin)
rules.add_perm("cafe.view_info_of_club", is_at_least_admin)
rules.add_perm("cafe.change_info_of_club", is_owner)
rules.add_perm("cafe.create_invite_for_club", is_owner)
rules.add_perm("cafe.create_delegated_levels_for_club", is_at_least_admin)
rules.add_perm("cafe.delete_club", is_owner)
