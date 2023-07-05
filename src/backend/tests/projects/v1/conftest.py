import pytest
import pytest_asyncio
from starlette.config import environ
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, drop_database, create_database
from httpx import AsyncClient

from alembic import command
from alembic.config import Config

import pathlib

# This sets `os.environ`, but provides some additional protection.
# If we placed it below the application import, it would raise an error
# informing us that 'TESTING' had already been read from the environment.
environ['TESTING'] = 'True'

from orchard.projects.v1.models.metadata import TEST_DATABASE_URL, metadata

# PROJECT_LOCATION is the path to app.py. behold and weep!
from orchard.projects.v1.app import app, __file__ as PROJECT_LOCATION

PATH_TO_ALEMBIC_INI = pathlib.Path(PROJECT_LOCATION).parent / "alembic.ini"

@pytest.fixture(scope="function", autouse=True)
def create_test_database():
    """
    Create a clean database on every test case.
    For safety, we should abort if a database already exists.

    We use the `sqlalchemy_utils` package here for a few helpers in consistently
    creating and dropping the database.
    """
    url = str(TEST_DATABASE_URL)
    assert not database_exists(url), 'Test database already exists. Aborting tests.'
    create_database(url)             # Create the test database.
    config = Config(str(PATH_TO_ALEMBIC_INI))   # Run the migrations.
    command.upgrade(config, "head")
    yield                            # Run the tests.
    drop_database(url)               # Drop the test database.


@pytest_asyncio.fixture
async def client():
    """
    When using the 'client' fixture in test cases, we'll get full database
    rollbacks between test cases:

    def test_homepage(client):
        url = app.url_path_for('homepage')
        response = client.get(url)
        assert response.status_code == 200
    """
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client

