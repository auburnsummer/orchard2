import contextlib
from typing import Type
from orchard.libs.melite.base import MeliteStruct
from orchard.libs.melite.migrations.migrate import migrate
from orchard.libs.melite.select import Select, T_co
from orchard.libs.melite.insert import insert as melite_insert
from orchard.libs.melite.update import update as melite_update
from orchard.libs.signal_fts5.install_extension import install_extension
from orchard.projects.v1.core.config import config
from orchard.projects.v1.migrations.all import ALL_MIGRATIONS
import apsw.bestpractice
import apsw

from loguru import logger

DATABASE_URL = config().DATABASE_URL
TEST_DATABASE_URL = "/tmp/test.db"
TESTING = config().TESTING

engine: apsw.Connection


def select(spec: Type[T_co]) -> Select[T_co]:
    "return a Select for the given type. pass a type in, not an instance of that type"
    return Select(engine, spec)

def insert(obj: MeliteStruct, recurse: bool = True):
    "inserts a struct into the db."
    return melite_insert(engine, obj, recurse)

def update(obj: MeliteStruct, recurse: bool = True):
    "updates a struct in the db."
    return melite_update(engine, obj, recurse)

def setup_db():
    global engine
    apsw.bestpractice.apply(apsw.bestpractice.recommended)
    if TESTING:
        engine = apsw.Connection(TEST_DATABASE_URL)
    else:
        engine = apsw.Connection(DATABASE_URL)
    install_extension(engine)
    migrate(engine, None, ALL_MIGRATIONS)


@contextlib.asynccontextmanager
async def lifespan(_):
    setup_db()
    yield
    engine.close() # not super necessary but nice to be safe