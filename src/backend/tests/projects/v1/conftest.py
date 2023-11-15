import contextlib
import os
from asgi_lifespan import LifespanManager
import pytest
import pytest_asyncio
from starlette.config import environ
from httpx import AsyncClient

import time_machine

# This sets `os.environ` before importing the app.
environ['TESTING'] = 'True'

from orchard.projects.v1 import app
from orchard.projects.v1.models.engine import TEST_DATABASE_URL

@pytest.fixture(scope="function", autouse=True)
def cleanup_test_database():
    """
    Create a clean database on every test case.
    For safety, we should abort if a database already exists.
    """
    yield    # Run the tests.
    with contextlib.suppress(FileNotFoundError):
        os.remove(TEST_DATABASE_URL)


@pytest_asyncio.fixture(scope="function")
async def client():
    """
    When using the 'client' fixture in test cases, we'll get full database
    rollbacks between test cases:

    def test_homepage(client):
        url = app.url_path_for('homepage')
        response = client.get(url)
        assert response.status_code == 200
    """
    async with LifespanManager(app) as manager:
        async with AsyncClient(app=manager.app, base_url="http://testserver") as c:
            yield c


@pytest.fixture(scope="function", autouse=True)
def time_is_a_human_construct():
    with time_machine.travel("2016-06-01"):
        yield