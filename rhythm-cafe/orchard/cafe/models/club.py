

from django.db import models

from .utils import create_pk_field
from cafe.libs.gen_id import IDType

class Club(models.Model):
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


class ClubMembership(models.Model):
    """
    A User can be a member of any number of Clubs. There are three levels of membership:

    - Owner: the user can add, remove and change users in the Club. Owners can demote other Owners.
    - Admin: the user can add/edit/delete levels under the Club.
    - Member: the user can add levels under the Club.
    """
    user = models.ForeignKey("cafe.User", on_delete=models.CASCADE)
    club = models.ForeignKey("cafe.Club", on_delete=models.CASCADE)

    role = models.CharField(choices={
        'owner': 'Owner',
        'admin': 'Admin',
        'member': 'Member'
    }, max_length=10)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'club'], name='unique_user_and_club')
        ]

class ClubRDLevel(models.Model):
    """
    An RDLevel can be included in more than one Club. Any Admin of the Club can edit/remove/etc any
    level within the Club.

    There's no additional metadata stored for now, but I'm making the through table now in anticipation
    to avoid a potentially annoying migration in the future.
    """
    rdlevel = models.ForeignKey("cafe.RDLevel", on_delete=models.CASCADE)
    club = models.ForeignKey("cafe.Club", on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['rdlevel', 'club'], name='unique_rdlevel_and_club')
        ]