# SQL models.
from typing import Annotated, TypeAlias
from fastapi import Depends
from sqlmodel import SQLModel, Session, create_engine

# import all sql models.
from v1.models.discord import DiscordMessage
from v1.models.level import Level
from v1.models.user import User
from v1.models.status import Status



sqlite_file_name = "orchard.sqlite3"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

InjectedSession: TypeAlias = Annotated[Session, Depends(get_session)]