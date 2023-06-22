"""
A User is an individual in the site.

Users are expected to have at least one Credential attached to them. This allows them to login with that Credential.

For the initial scope, the only Credential planned is Discord login.
"""

from pydantic import BaseModel
from .metadata import database, metadata
from uuid import uuid4

import sqlalchemy as sa

users = sa.Table(
    "users",
    metadata,
    sa.Column("id", sa.String, primary_key=True),
    sa.Column("name", sa.String)
)

class User(BaseModel):
    id: str
    name: str

    def to_dict(self):
        return self.model_dump()


class UserNotFoundException(Exception):
    pass


async def get_user_by_id(id: str):
    query = users.select().where(users.c.id == id)
    result = await database.fetch_one(query)
    if result:
        return User(**result)
    else:
        raise UserNotFoundException(f"The user with id {id} was not found.")


async def get_all_users():
    query = users.select()
    results = await database.fetch_all(query)
    return [User(**result) for result in results]


async def add_user(name: str):
    new_id = uuid4().hex
    query = users.insert().values(
        id=new_id,
        name=name
    )
    await database.execute(query)
    resultant_user = await get_user_by_id(new_id)
    return resultant_user