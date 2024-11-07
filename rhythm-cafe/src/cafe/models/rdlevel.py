from operator import is_
from django.db import models

from django.db.models import Q


from .utils import create_pk_field
from cafe.libs.gen_id import IDType
from rules.contrib.models import RulesModel
import rules

@rules.predicate
def is_at_least_admin_of_connected_club(user, level: "RDLevel"):
    return True

@rules.predicate
def is_submitter(user, level: "RDLevel"):
    return level.submitter == user

can_change = rules.is_authenticated & (rules.is_superuser | is_at_least_admin_of_connected_club | is_submitter)

class RDLevel(RulesModel):
    """
    An RDLevel represents a single Rhythm Doctor level.
    """
    id = create_pk_field(IDType.RD_LEVEL)

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

    submitter = models.ForeignKey("cafe.User", on_delete=models.CASCADE)

    club = models.ForeignKey("cafe.Club", on_delete=models.CASCADE)

    class Meta:
        rules_permissions = {
            # cafe.change_rdlevel
            "change": can_change,
            # cafe.delete_rdlevel
            "delete": can_change
        }