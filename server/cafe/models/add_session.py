from django.db import models

from cafe.models.rdlevels.prefill import RDLevelPrefillResult


class AddSessionPhase(models.IntegerChoices):
    # Normal flow
    SELECTING_ATTACHMENT = 1  # multiple attachments — user picks which one
    SELECTING_TYPE = 2        # user picks "new" or "update"
    UPLOADING = 3             # prefill task is running
    COMPLETE = 4              # prefill done, show results/link
    # Error states
    ERROR_LEVEL_NOT_FOUND = 5   # user entered an update level ID that doesn't exist
    ERROR_NO_PERMISSION = 6     # user doesn't have permission to edit that level
    ERROR_DUPLICATE = 7         # update rejected — a level with the same SHA1 already exists


class AddSession(models.Model):
    """
    An AddSession represents a user's progress in the multi-step process of adding a level from a Discord attachment.
    """
    # this is equal to the interaction ID from Discord, which is guaranteed to be unique, so we can use it as the PK.
    id = models.TextField(primary_key=True)

    # user who will be credited as the submitter of the level being added.
    # nb: this may not be the user that initiated the add session, e.g. delegated scenario
    user = models.ForeignKey("cafe.User", on_delete=models.CASCADE)

    # application_id = DISCORD_CLIENT_ID env

    # token used to send followup messages/interactions to discord, valid for 15 minutes after the initial interaction is received
    interaction_token = models.TextField()

    phase = models.IntegerField(choices=AddSessionPhase.choices, default=AddSessionPhase.SELECTING_ATTACHMENT)

    prefill = models.ForeignKey(RDLevelPrefillResult, blank=True, null=True, default=None, on_delete=models.CASCADE)

    # the attachments from the original Discord message, stored as a JSON array. 
    # nb: the attachments are only sent in the initial interaction so we need to store them here for later phases.
    # why store ALL attachments? cause they can go back to phase 1 and select a different one
    attachments = models.JSONField()

    # the URL of the attachment the user is adding. This is set in phase 1, and used in phase 2 to prefill the add form.
    selected_attachment_url = models.TextField(null=True, blank=True)

    # if the addsession state is for "new" or "update".
    add_type = models.CharField(max_length=10, default="new")