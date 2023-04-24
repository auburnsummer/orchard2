from sqlmodel import Field, Relationship, SQLModel, create_engine, JSON, Column


class User(SQLModel, table=True):
    discord_id: str = Field(primary_key=True)
    # if True, levels posted by this user to a showcase channel can be added by _anyone_.
    # NB: if the level has :no-entry-sign: it still cannot be added, even if this is True.
    anyone_can_add: bool = Field(default=True)
    # if True, the user cannot add or modify levels.
    banned: bool = Field(default=False) 