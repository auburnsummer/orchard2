"""
A Guild Credential is an identifier for a publisher.

A discord guild can only be part of one publisher.
"""

from .metadata import engine, metadata

import sqlalchemy as sa

import msgspec

disc_guild_credentials = sa.Table(
    "discord_guild_credentials",
    metadata,
    sa.Column("id", sa.String, primary_key=True),
    sa.Column("publisher_id", sa.String, sa.ForeignKey("publishers.id"))
)