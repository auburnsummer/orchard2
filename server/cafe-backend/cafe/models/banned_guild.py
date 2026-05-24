from django.db import models


class BannedGuild(models.Model):
    """
    A BannedGuild is a Discord server (guild) that is prohibited from
    using the Discord bot.
    """
    guild_id = models.TextField(unique=True)
    reason = models.TextField(blank=True)
    banned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Banned guild: ({self.guild_id})"
