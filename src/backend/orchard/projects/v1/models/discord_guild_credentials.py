"""
A Guild Credential is an identifier for a publisher.

A discord guild can only be part of one publisher, although a publisher can span multiple discord guilds.
"""
from __future__ import annotations
from orchard.projects.v1.core.exceptions import DiscordGuildCredentialAlreadyExists

from sqlalchemy.ext.asyncio import AsyncConnection
from .metadata import engine, metadata

import sqlalchemy as sa

import msgspec

from typing import TYPE_CHECKING
from orchard.projects.v1.models.publishers import add_publisher


if TYPE_CHECKING:
    from orchard.projects.v1.models.publishers import Publisher


disc_guild_credentials = sa.Table(
    "discord_guild_credentials",
    metadata,
    sa.Column("id", sa.String, primary_key=True),
    sa.Column("publisher_id", sa.String, sa.ForeignKey("publishers.id"))
)

class DiscordGuildCredentialNotFoundException(Exception):
    pass


class DiscordGuildCredential(msgspec.Struct):
    id: str
    publisher_id: str

    def to_dict(self):
        return msgspec.structs.asdict(self)


async def get_disc_guild_credential(credential_id: str, conn: AsyncConnection):
    query = disc_guild_credentials.select().where(disc_guild_credentials.c.id == credential_id)
    result = (await conn.execute(query)).first()
    if result:
        return msgspec.convert(result._mapping, DiscordGuildCredential)
    else:
        raise DiscordGuildCredentialNotFoundException(f"The cred with id {credential_id} was not found.")


async def create_disc_guild_credential(credential_id: str, publisher: Publisher, conn: AsyncConnection):
    query = disc_guild_credentials.insert().values(
        id=credential_id,
        publisher_id=publisher.id
    )
    await conn.execute(query)
    resultant_credential = await get_disc_guild_credential(credential_id, conn)
    return resultant_credential



async def make_new_publisher_with_credential(credential_id: str, name: str, conn: AsyncConnection):
    try:
        _ = await get_disc_guild_credential(credential_id, conn)
        raise DiscordGuildCredentialAlreadyExists(credential_id=credential_id)
    except DiscordGuildCredentialNotFoundException:
        pass
    except Exception as e:
        raise e
    publisher = await add_publisher(name, conn)
    cred = await create_disc_guild_credential(credential_id, publisher, conn)
    return publisher, cred 