"""
A Publisher is a source that levels come from (e.g. RDL, RWU).

All levels belong to a Publisher and a User. Publishers are able to perform admin tasks
relating specifically to levels under their scope.

Which users are "admin users", etc. is handled internally within the Publisher. For instance,
with the Discord server implementation of a Publisher, slash command permissions are used to
determine who can access admin capabilities.

"Self publishing" a level will be possible. Creating a Publisher should be self-service.

For the initial scope, the only implementation of a publisher is a Discord server.
"""
from __future__ import annotations
from datetime import datetime, timezone
from orchard.libs.melite.base import MeliteStruct
from orchard.libs.utils.gen_id import IDType, gen_id
from orchard.projects.v1.models.engine import insert

class Publisher(MeliteStruct):
    table_name = "publisher"

    id: str
    name: str
    cutoff: datetime = datetime.fromtimestamp(0, tz=timezone.utc)

    @staticmethod
    def new(name: str) -> Publisher:
        "Creates a new publisher with the specified name but does not insert that user into the db."
        return Publisher(
            id=gen_id(IDType.PUBLISHER),
            name=name
        )

    @staticmethod
    def create(name: str) -> Publisher:
        "Creates a new user with the specified name and inserts that user into the db."
        new_publisher = Publisher.new(name)
        insert(new_publisher)
        return new_publisher
