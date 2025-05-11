from __future__ import annotations
from operator import is_
from django.db import models
from cafe.models.id_utils import generate_rdlevel_id, RDLEVEL_ID_LENGTH
from cafe.models.types import UserType, ClubType

from django.db.models import Q

from rules.contrib.models import RulesModel
import rules
@rules.predicate
def is_at_least_admin_of_connected_club(user: UserType, level: "RDLevel"):
    memberships = user.memberships.filter(club__exact=level.club, role__in=["owner", "admin"])
    return len(memberships) > 0

@rules.predicate
def is_submitter(user: UserType, level: "RDLevel"):
    return level.submitter == user

can_change = rules.is_authenticated & (rules.is_superuser | is_at_least_admin_of_connected_club | is_submitter)


class RDLevel(RulesModel):
    """
    An RDLevel represents a single Rhythm Doctor level.
    """
    id = models.CharField(max_length=RDLEVEL_ID_LENGTH, primary_key=True, default=generate_rdlevel_id)

    artist = models.TextField(blank=False)
    artist_tokens = models.JSONField(blank=False)

    song = models.TextField(blank=False)
    song_alt = models.TextField(blank=True)

    seizure_warning = models.BooleanField(blank=False)
    description = models.TextField(blank=True)

    hue = models.FloatField(blank=False)
    authors = models.JSONField(blank=False)
    authors_raw = models.TextField(blank=False)
    max_bpm = models.IntegerField(blank=False)
    min_bpm = models.IntegerField(blank=False)

    difficulty = models.IntegerField(blank=False)
    single_player = models.BooleanField(blank=False)
    two_player = models.BooleanField(blank=False)
    last_updated = models.DateTimeField(blank=False)
    tags = models.JSONField(blank=False)
    has_classics = models.BooleanField(blank=False)
    has_oneshots = models.BooleanField(blank=False)
    has_squareshots = models.BooleanField(blank=False)
    has_freezeshots = models.BooleanField(blank=False)
    has_freetimes = models.BooleanField(blank=False)
    has_holds = models.BooleanField(blank=False)
    has_skipshots = models.BooleanField(blank=False)
    has_window_dance = models.BooleanField(blank=False)

    sha1 = models.TextField(blank=False, unique=True)
    rdlevel_sha1 = models.TextField(blank=False)
    is_animated = models.BooleanField(blank=False)

    rdzip_url = models.TextField(blank=False)
    image_url = models.TextField(blank=False)
    thumb_url = models.TextField(blank=False)
    icon_url = models.TextField(blank=True, default="")

    submitter = models.ForeignKey(UserType, on_delete=models.CASCADE)

    club = models.ForeignKey(ClubType, on_delete=models.CASCADE)

    approval = models.IntegerField(blank=False, default=0)

    def __str__(self):
        return f"{self.song} ({self.id})"

    def to_dict(self):
        return {
            "id": self.id,
            "artist": self.artist,
            "artist_tokens": self.artist_tokens,
            "song": self.song,
            "song_alt": self.song_alt,
            "seizure_warning": self.seizure_warning,
            "description": self.description,
            "hue": self.hue,
            "authors": self.authors,
            "max_bpm": self.max_bpm,
            "min_bpm": self.min_bpm,
            "difficulty": self.difficulty,
            "single_player": self.single_player,
            "two_player": self.two_player,
            "last_updated": self.last_updated.isoformat(),
            "tags": self.tags,
            "has_classics": self.has_classics,
            "has_oneshots": self.has_oneshots,
            "has_squareshots": self.has_squareshots,
            "has_freezeshots": self.has_freezeshots,
            "has_freetimes": self.has_freetimes,
            "has_holds": self.has_holds,
            "has_skipshots": self.has_skipshots,
            "has_window_dance": self.has_window_dance,
            "sha1": self.sha1,
            "rdlevel_sha1": self.rdlevel_sha1,
            "is_animated": self.is_animated,
            "rdzip_url": self.rdzip_url,
            "image_url": self.image_url,
            "thumb_url": self.thumb_url,
            "icon_url": self.icon_url,
            "submitter": self.submitter.to_dict(),
            "club": self.club.to_dict(),
            "approval": self.approval
        }

    class Meta:
        rules_permissions = {
            # cafe.change_rdlevel
            "change": can_change,
            # cafe.delete_rdlevel
            "delete": can_change
        }