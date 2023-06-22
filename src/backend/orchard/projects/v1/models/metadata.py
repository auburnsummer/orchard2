import databases
import sqlalchemy as sa

from orchard.projects.v1.core.config import config

DATABASE_URL = config().DATABASE_URL

metadata = sa.MetaData()

database = databases.Database(DATABASE_URL)

import contextlib

@contextlib.asynccontextmanager
async def lifespan(app):
    await database.connect()
    yield
    await database.disconnect()
