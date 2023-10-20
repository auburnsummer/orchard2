"""
A Publisher is a source that levels come from (e.g. RDL, RWU)

All levels belong to a Publisher and a User. Publishers are able to perform admin tasks
relating specifically to levels under their scope.

Which users are "admin users", etc. is handled internally within the Publisher. For instance,
with the Discord server implementation of a Publisher, slash command permissions are used to
determine who can access admin capabilities.

"Self publishing" a level will be possible. Creating a Publisher should be self-service.

For the initial scope, the only implementation of a publisher is a Discord server.
"""
from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING
from orchard.libs.utils.gen_id import IDType, gen_id

from sqlalchemy.ext.asyncio import AsyncConnection

from orchard.projects.v1.models.metadata import metadata

import sqlalchemy as sa

import msgspec

if TYPE_CHECKING:
    from orchard.projects.v1.models.discord_guild_credentials import DiscordGuildCredential


publishers = sa.Table(
    "publishers",
    metadata,
    sa.Column("id", sa.String, primary_key=True),
    sa.Column("name", sa.String, nullable=False), 
    sa.Column("cutoff", sa.DateTime, nullable=False),
)

class PublisherNotFoundException(Exception):
    pass


class Publisher(msgspec.Struct):
    id: str
    name: str
    cutoff: datetime = datetime.utcfromtimestamp(0)

    def to_dict(self):
        return msgspec.structs.asdict(self)


async def get_all_publishers(conn: AsyncConnection):
    query = publishers.select()
    results = (await conn.execute(query)).all()

    return [msgspec.convert(result._mapping, Publisher) for result in results]


async def get_publisher_by_id(id: str, conn: AsyncConnection):
    query = publishers.select().where(publishers.c.id == id)
    result = (await conn.execute(query)).first()

    if result:
        return msgspec.convert(result._mapping, Publisher)
    else:
        raise PublisherNotFoundException(f"The user with id {id} was not found.")

    
async def get_publisher_by_discord_guild_credential(cred: DiscordGuildCredential, conn: AsyncConnection):
    id = cred.publisher_id
    return await get_publisher_by_id(id, conn)

    

async def add_publisher(name: str, conn: AsyncConnection):
    new_id = gen_id(IDType.PUBLISHER)
    publisher = Publisher(id=new_id, name=name)

    query = publishers.insert().values(publisher.to_dict())
    await conn.execute(query)

    resultant_publisher = await get_publisher_by_id(new_id, conn)
    return resultant_publisher


