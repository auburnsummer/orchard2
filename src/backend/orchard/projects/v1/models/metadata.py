import databases
import sqlalchemy as sa

from orchard.projects.v1.core.config import config

DATABASE_URL = config().DATABASE_URL
TEST_DATABASE_URL = "sqlite:////tmp/test.db"
TESTING = config().TESTING

metadata = sa.MetaData()

if TESTING:
    database = databases.Database(TEST_DATABASE_URL, force_rollback=True)
else:
    database = databases.Database(DATABASE_URL)

import contextlib

@contextlib.asynccontextmanager
async def lifespan(app):
    await database.connect()
    yield
    await database.disconnect()
