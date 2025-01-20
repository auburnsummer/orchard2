from __future__ import annotations
from typing import TYPE_CHECKING, TypeAlias

from rules.contrib.models import RulesModel
from django.db import models

if TYPE_CHECKING:
    from cafe.models.user import User
    from cafe.models.clubs.club import Club

# work around pylance
# https://github.com/microsoft/pylance-release/issues/5124#issuecomment-1814901159
_User: TypeAlias = "User"
_Club: TypeAlias = "Club"


class ClubMembership(RulesModel):
    """
    A User can be a member of any number of Clubs. There are two levels of membership:

    - Owner: the user can add, remove and change users in the Club. Owners can demote other Owners.
    - Admin: the user can add/edit/delete levels under the Club.

    nb: a club can also be linked to a discord server. Anyone who has access to the
    discord server can also add levels, even if they're not an Admin.
    """
    user = models.ForeignKey(_User, on_delete=models.CASCADE, related_name="memberships")
    club = models.ForeignKey(_Club, on_delete=models.CASCADE, related_name="memberships")

    role = models.TextField(choices=[
        ('owner', 'Owner'),
        ('admin', 'Admin')
    ])

    def __str__(self):
        return f"{self.user} -> {self.club} [{self.role}]"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'club'], name='unique_user_and_club')
        ]
