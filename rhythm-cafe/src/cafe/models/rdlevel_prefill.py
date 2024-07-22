from rules.contrib.models import RulesModel
from django.db import models

from .utils import create_pk_field
from cafe.libs.gen_id import IDType


class RDLevelPrefillResult(RulesModel):
    """
    A prefill result stores the initial analysis of an rdzip file.
    This is stored as an opaque blob (...it's json, but whatever)
    """
    id = create_pk_field(IDType.PREFILL)
    ready = models.BooleanField(default=False)
    data = models.TextField(default="")
