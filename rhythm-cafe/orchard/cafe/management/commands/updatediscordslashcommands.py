"""
It's pretty uncommon to add new commands (I hope),

so this is a one off command that we run via manage.py
"""

from django.core.management.base import BaseCommand, CommandError
from cafe.views.discord_bot.register_commands import register_commands

class Command(BaseCommand):
    help = "Updates discord bot commands"

    def handle(self, *args, **options):
        bot_token = input("Copy paste bot token here:")
        register_commands(bot_token)