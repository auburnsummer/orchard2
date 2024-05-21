from django.db import models

from .utils import create_pk_field
from cafe.libs.gen_id import IDType

class Publisher(models.Model):
    """
    A Publisher is a source where levels come from (RDL, RWU, etc.)

    Users can be admins of Publishers. This is just done via permissions.
    todo: each Publisher should have a permission associated with it.
    """
    id = create_pk_field(IDType.PUBLISHER)
    name = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.name} ({self.id})"