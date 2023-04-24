from sqlmodel import Field, Relationship, SQLModel, create_engine, JSON, Column
from typing import Optional
import datetime

class Status(SQLModel, table=True):
    alias: str = Field(primary_key=True)

    level_id: str = Field(foreign_key="level.rdlevel_sha1")

    approval: int = Field(default=0)
    approval_thread: Optional[str] = Field(default=None)

    approved_time: Optional[datetime.datetime] = Field(default=None)

