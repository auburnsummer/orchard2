"""
A Credential is a method that a User can use to log in.

A Credential can only be used to log into a specific User. However, a User can have multiple Credentials.

The only Credential type available is Discord at the moment.
"""
from __future__ import annotations

from orchard.libs.melite.base import MeliteStruct
from orchard.projects.v1.models.engine import insert, select
from orchard.projects.v1.models.users import User

class DiscordCredential(MeliteStruct):
    table_name = "discord_credential"

    id: str
    user: User

    @staticmethod
    def get_or_create(id_: str, name_if_doesnt_exist: str):
        """
        Get a DiscordCredential, or creates it with the specified name and underlying user.
        nb: A DiscordCredential always exists with a user.
        """
        cred = select(DiscordCredential).by_id(id_)
        if not cred:
            # make a new user.
            user = User.new(name=name_if_doesnt_exist)
            cred = DiscordCredential(id=id_, user=user)
            insert(cred) # the user is inserted also.
        return cred