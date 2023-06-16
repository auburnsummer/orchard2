# SQL models.
from typing import Annotated, TypeAlias
from fastapi import Depends
from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy.future import Engine

# because SQLModel.metadata.create_all works by seeing what SQLModel subclasses are
# accessible from the current scope, we need to import all models here. (even though
# we don't use them in this file)
from v1.models.discord import DiscordMessage
from v1.models.level import Level
from v1.models.user import User
from v1.models.status import Status

from v1.libs.env import env

engine_singleton: Engine | None = None

def _get_engine() -> Engine:
    global engine_singleton
    if engine_singleton is None:
        connect_args = {"check_same_thread": False}
        session_url = f"sqlite:///{env().orchard_db_path}"
        engine_singleton = create_engine(session_url, echo=True, connect_args=connect_args)
    return engine_singleton

def create_db_and_tables():
    engine = _get_engine()
    SQLModel.metadata.create_all(engine)

def get_session():
    engine = _get_engine()
    with Session(engine) as session:
        yield session

InjectedSession: TypeAlias = Annotated[Session, Depends(get_session)]