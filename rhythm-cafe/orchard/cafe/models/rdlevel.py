from django.db import models

from .utils import create_pk_field
from cafe.libs.gen_id import IDType


class RDLevel(models.Model):
    """
    An RDLevel represents a single Rhythm Doctor level.
    """
    id = create_pk_field(IDType.RD_LEVEL)
    song = models.TextField(blank=False)
    