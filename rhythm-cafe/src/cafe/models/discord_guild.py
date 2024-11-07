from django.db import models

from cafe.models import Club


class DiscordGuild(models.Model):
    """
    An DiscordGuild is a Discord server.

    The id is the discord id.

    Guilds can be associated with up to one Club. This allows certain slash commands
    used within the guild to work with the Club.
    """
    id = models.TextField(primary_key=True)

    club = models.ForeignKey(Club, on_delete=models.CASCADE, null=True, related_name="discord_guilds")
