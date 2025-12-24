from __future__ import annotations
from django.db import models
from django.db.models import Manager

from cafe.models.id_utils import generate_rdlevel_id, RDLEVEL_ID_LENGTH
from cafe.models.types import UserType, ClubType

from simple_history.models import HistoricalRecords

from rules.contrib.models import RulesModel
import rules

from cafe.tasks.sync_level_to_typesense import sync_level_to_typesense
from cafe.models.clubs.predicates import is_pharmacist

@rules.predicate
def is_at_least_admin_of_connected_club(user: UserType, level: "RDLevel"):
    memberships = user.memberships.filter(club__exact=level.club, role__in=["owner", "admin"])
    return len(memberships) > 0

@rules.predicate
def is_submitter(user: UserType, level: "RDLevel"):
    return level.submitter == user

can_change = rules.is_authenticated & (rules.is_superuser | is_pharmacist | is_at_least_admin_of_connected_club | is_submitter)

can_delete = rules.is_authenticated & (rules.is_superuser | is_at_least_admin_of_connected_club | is_submitter | is_pharmacist)

can_review = rules.is_authenticated & (rules.is_superuser | is_pharmacist)

can_blend = can_review

class RDLevel(RulesModel):
    """
    An RDLevel represents a single Rhythm Doctor level.
    """
    id = models.CharField(max_length=RDLEVEL_ID_LENGTH, primary_key=True, default=generate_rdlevel_id)

    artist = models.TextField(blank=False)
    artist_tokens = models.JSONField(blank=False)
    artist_raw = models.TextField(blank=False, default="")

    song = models.TextField(blank=False)
    song_alt = models.TextField(blank=True)

    song_raw = models.TextField(blank=False, default="")

    seizure_warning = models.BooleanField(blank=False)
    description = models.TextField(blank=True)

    hue = models.FloatField(blank=False)
    authors = models.JSONField(blank=False)
    authors_raw = models.TextField(blank=False, default="")
    max_bpm = models.IntegerField(blank=False)
    min_bpm = models.IntegerField(blank=False)

    difficulty = models.IntegerField(blank=False)
    single_player = models.BooleanField(blank=False)
    two_player = models.BooleanField(blank=False)
    last_updated = models.DateTimeField(blank=False)
    tags = models.JSONField(blank=False)

    sha1 = models.TextField(blank=False, unique=True)
    rdlevel_sha1 = models.TextField(blank=False)
    rd_md5 = models.TextField(blank=False, default="")
    is_animated = models.BooleanField(blank=False)

    rdzip_url = models.TextField(blank=False)
    image_url = models.TextField(blank=False)
    thumb_url = models.TextField(blank=False)
    icon_url = models.TextField(blank=True, default="")

    submitter = models.ForeignKey(UserType, on_delete=models.CASCADE)

    club = models.ForeignKey(ClubType, on_delete=models.CASCADE)

    approval = models.IntegerField(blank=False, default=0)

    approval_notes_private = models.TextField(blank=True, default="")
    approval_notes_public = models.TextField(blank=True, default="")

    is_private = models.BooleanField(blank=False, default=False)

    prefill_version = models.IntegerField(blank=False, default=0)

    history = HistoricalRecords()

    def __str__(self):
        return f"{self.song} ({self.id})"

    def to_dict(self):
        return {
            "id": self.id,
            "artist": self.artist,
            "artist_tokens": self.artist_tokens,
            "artist_raw": self.artist_raw,
            "song": self.song,
            "song_alt": self.song_alt,
            "song_raw": self.song_raw,
            "seizure_warning": self.seizure_warning,
            "description": self.description,
            "hue": self.hue,
            "authors": self.authors,
            "authors_raw": self.authors_raw,
            "max_bpm": self.max_bpm,
            "min_bpm": self.min_bpm,
            "difficulty": self.difficulty,
            "single_player": self.single_player,
            "two_player": self.two_player,
            "last_updated": self.last_updated.isoformat(),
            "tags": self.tags,
            "sha1": self.sha1,
            "rdlevel_sha1": self.rdlevel_sha1,
            "rd_md5": self.rd_md5,
            "is_animated": self.is_animated,
            "rdzip_url": self.rdzip_url,
            "image_url": self.image_url,
            "thumb_url": self.thumb_url,
            "icon_url": self.icon_url,
            "submitter": self.submitter.to_dict(),
            "club": self.club.to_dict(),
            "approval": self.approval,
            "approval_notes_public": self.approval_notes_public,
            "is_private": self.is_private,
            "prefill_version": self.prefill_version
            # private notes are not included in to_dict as to_dict is used for public APIs
        }

    def save(self, *args, **kwargs):
        super(RDLevel, self).save(*args, **kwargs)
        sync_level_to_typesense(self.id)

    def delete(self, *args, **kwargs):
        super(RDLevel, self).delete(*args, **kwargs)
        sync_level_to_typesense(self.id)

    class Meta:
        rules_permissions = {
            # cafe.change_rdlevel
            "change": can_change,
            # cafe.delete_rdlevel
            "delete": can_delete,
            # cafe.peerreview_rdlevel
            "peerreview": can_review,
            # cafe.blend_rdlevel
            "blend": can_blend
        }