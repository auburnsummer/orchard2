from __future__ import annotations
from typing import TYPE_CHECKING, TypeAlias

import rules
from rules.contrib.models import RulesModel
from django.db import models

from cafe.models.clubs.predicates import is_owner_of_permission_club, is_permission_subject
from cafe.models.types import UserType, ClubType

class ClubMembership(RulesModel):
    """
    A User can be a member of any number of Clubs. There are two levels of membership:

    - Owner: the user can add, remove and change users in the Club. Owners can demote other Owners.
    - Admin: the user can add/edit/delete levels under the Club, even levels they didn't post.

    nb: a club can also be linked to a discord server. Anyone who has access to the
    discord server can also add levels, even if they're not an Admin.
    """
    user = models.ForeignKey(UserType, on_delete=models.CASCADE, related_name="memberships")
    club = models.ForeignKey(ClubType, on_delete=models.CASCADE, related_name="memberships")

    role = models.TextField(choices=[
        ('owner', 'Owner'),
        ('admin', 'Admin')
    ])

    def __str__(self):
        return f"{self.user} -> {self.club} [{self.role}]"
    
    def to_dict(self):
        return {
            "user": self.user.to_dict(),
            "club": self.club.to_dict(),
            "role": self.role
        }

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'club'], name='unique_user_and_club')
        ]

        rules_permissions = {
            # cafe.change_clubmembership
            "change": is_owner_of_permission_club,
            # cafe.delete_clubmembership
            "delete": is_owner_of_permission_club | is_permission_subject
        }
