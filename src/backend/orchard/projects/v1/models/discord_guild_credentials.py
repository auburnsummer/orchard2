"""
A Guild Credential is an identifier for a publisher.

A discord guild can only be part of one publisher, although a publisher can span multiple discord guilds.
"""
from __future__ import annotations

from orchard.libs.melite.base import MeliteStruct
from orchard.projects.v1.models.publishers import Publisher

class DiscordGuildPublisherCredential(MeliteStruct):
    table_name = "discord_guild_publisher_credential"

    id: str
    publisher: Publisher
    
