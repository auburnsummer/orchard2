from django.db import models

from .utils import create_pk_field
from cafe.libs.gen_id import IDType


class DiscordGuild(models.Model):
    """
    An DiscordGuild is a Discord server.

    The id is the discord id.

    There isn't anything else here yet, but we're using it in case we end up storing
    discord-specific info in the future.
    """
    id = models.TextField(primary_key=True)
    