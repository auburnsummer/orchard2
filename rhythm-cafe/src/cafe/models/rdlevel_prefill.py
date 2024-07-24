from rules.contrib.models import RulesModel
from django.db import models

from .utils import create_pk_field
from cafe.libs.gen_id import IDType

from cafe.models import User, Club


class RDLevelPrefillResult(RulesModel):
    """
    A prefill result stores the initial analysis of an rdzip file.
    This is stored as an opaque blob (...it's json, but whatever)
    """
    id = create_pk_field(IDType.PREFILL)
    # task will set to True when the task is complete.
    ready = models.BooleanField(default=False)
    # generated by the prefill task.
    data = models.TextField(default="")
    # the user that initiated the prefill.
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, default=None)
    # the club that the prefill is allowed to be used for.
    club = models.ForeignKey(Club, on_delete=models.CASCADE, blank=True, null=True, default=None)
    # errors that occurred during the prefill.
    errors = models.TextField(default="")
