# import databases
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from orchard.projects.v1.core.config import config

DATABASE_URL = config().DATABASE_URL
TEST_DATABASE_URL = "sqlite+aiosqlite:////tmp/test.db"
TESTING = config().TESTING

metadata = sa.MetaData()

engine: AsyncEngine
if TESTING:
    engine = create_async_engine(TEST_DATABASE_URL)
else:
    engine = create_async_engine(DATABASE_URL)

import contextlib

@contextlib.asynccontextmanager
async def lifespan(app):
    async with engine.begin() as conn:
        await conn.exec_driver_sql("PRAGMA foreign_keys=ON;")
    yield
    await engine.dispose()