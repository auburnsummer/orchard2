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
from datetime import datetime
from .metadata import engine, metadata

import sqlalchemy as sa

import msgspec

publishers = sa.Table(
    "publishers",
    metadata,
    sa.Column("id", sa.String, primary_key=True),
    sa.Column("name", sa.String, nullable=False),
    sa.Column("cutoff", sa.DateTime, nullable=False),
)

class Publisher(msgspec.Struct):
    id: str
    name: str
    cutoff: datetime

    def to_dict(self):
        return msgspec.structs.asdict(self)

