"""
A Credential is a method that a User can use to log in.

A Credential can only be used to log into one User. However, a User can have multiple Credentials.

The only Credential type available is Discord at the moment.
"""
from __future__ import annotations

import sqlalchemy as sa

from .metadata import metadata, engine

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from orchard.projects.v1.models.users import User

import msgspec

discord_credentials = sa.Table(
    "discord_credentials",
    metadata,
    sa.Column("id", sa.String, primary_key=True),
    sa.Column("user_id", sa.String, sa.ForeignKey("users.id"))
)

class DiscordCredential(msgspec.Struct):
    id: str
    user_id: str

    def to_dict(self):
        return msgspec.structs.asdict(self)


class DiscordCredentialNotFoundException(Exception):
    pass


async def get_disc_credential(credential_id: str):
    async with engine.begin() as conn:
        query = discord_credentials.select().where(discord_credentials.c.id == credential_id)
        result = (await conn.execute(query)).first()
    if result:
        return msgspec.convert(result._mapping, DiscordCredential)
    else:
        raise DiscordCredentialNotFoundException(f"The user with id {id} was not found.")


async def create_credential(credential_id: str, user: User):
    async with engine.begin() as conn:
        query = discord_credentials.insert().values(
            id=credential_id,
            user_id=user.id
        )
        await conn.execute(query)
    resultant_credential = await get_disc_credential(credential_id)
    return resultant_credential


async def make_new_user_with_credential(credential_id: str, name: str):
    from orchard.projects.v1.models.users import add_user

    user = await add_user(name)
    cred = await create_credential(credential_id, user)
    return user, cred


async def create_or_get_user_with_credential(credential_id: str, name: str):
    from orchard.projects.v1.models.users import get_user_by_discord_credential

    cred: DiscordCredential
    try:
        existing_cred = await get_disc_credential(credential_id)
        cred = existing_cred
    except DiscordCredentialNotFoundException:
        _, new_cred = await make_new_user_with_credential(credential_id, name)
        cred = new_cred
    user = await get_user_by_discord_credential(cred)
    return user, cred