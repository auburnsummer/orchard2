from django.db import models
from django.utils import timezone
from typing import TYPE_CHECKING, TypeAlias

if TYPE_CHECKING:
    from cafe.models.clubs.club import Club

# work around pylance
# https://github.com/microsoft/pylance-release/issues/5124#issuecomment-1814901159
_Club: TypeAlias = "Club"


class ClubInvite(models.Model):
    """
    A ClubInvite allows a user to join a Club. They can only be used once; it's deleted from the db after use.
    """
    club = models.ForeignKey(_Club, on_delete=models.CASCADE)
    role = models.TextField(choices=[
        ('owner', 'Owner'),
        ('admin', 'Admin')
    ])
    expiry = models.DateTimeField()
    code = models.CharField(max_length=100)

    def has_expired(self):
        return timezone.now() > self.expiry

    def __str__(self):
        return f"Invite to {self.club} as {self.role}, expires {self.expiry}"