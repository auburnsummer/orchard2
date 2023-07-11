import os
import pytest
import pytest_asyncio
from starlette.config import environ
from httpx import AsyncClient

from alembic import command
from alembic.config import Config

import pathlib

import time_machine

# This sets `os.environ`, but provides some additional protection.
# If we placed it below the application import, it would raise an error
# informing us that 'TESTING' had already been read from the environment.
environ['TESTING'] = 'True'

from orchard.projects.v1.models.metadata import TEST_DATABASE_URL

# PROJECT_LOCATION is the path to app.py. behold and weep!
from orchard.projects.v1.app import app, __file__ as PROJECT_LOCATION

PATH_TO_ALEMBIC_INI = pathlib.Path(PROJECT_LOCATION).parent / "alembic.ini"

@pytest.fixture(scope="function", autouse=True)
def create_test_database():
    """
    Create a clean database on every test case.
    For safety, we should abort if a database already exists.
    """
    url = str(TEST_DATABASE_URL)
    config = Config(str(PATH_TO_ALEMBIC_INI))   # Run the migrations.
    command.upgrade(config, "head")
    yield                            # Run the tests.
    os.remove(url.replace("sqlite+aiosqlite:///", ""))


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


@pytest.fixture(scope="function", autouse=True)
def time_is_a_human_construct():
    with time_machine.travel("2016-06-01"):
        yield