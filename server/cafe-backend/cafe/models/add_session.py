from django.db import models

from cafe.models.rdlevels.prefill import RDLevelPrefillResult


class AddSession(models.Model):
    """
    An AddSession represents a user's progress in the multi-step process of adding a level from a Discord attachment.
    """
    # this is equal to the interaction ID from Discord, which is guaranteed to be unique, so we can use it as the PK.
    id = models.TextField(primary_key=True)

    # application_id = DISCORD_CLIENT_ID env

    # token used to send followup messages/interactions to discord, valid for 15 minutes after the initial interaction is received
    interaction_token = models.TextField()

    # the current phase of the add flow the user is on. I will later make an ascii state diagram
    phase = models.IntegerField(default=1)

    prefill = models.ForeignKey(RDLevelPrefillResult, blank=True, null=True, default=None, on_delete=models.CASCADE)

    # the attachments from the original Discord message, stored as a JSON array. 
    # nb: the attachments are only sent in the initial interaction so we need to store them here for later phases.
    # why store ALL attachments? cause they can go back to phase 1 and select a different one
    attachments = models.JSONField()

    # the URL of the attachment the user is adding. This is set in phase 1, and used in phase 2 to prefill the add form.
    selected_attachment_url = models.TextField(null=True, blank=True)

    # if the addsession state is for "new" or "update".
    add_type = models.CharField(max_length=10, default="new")