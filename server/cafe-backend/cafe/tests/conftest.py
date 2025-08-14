import pytest

@pytest.fixture
def environment(autouse=True):
    import os
    os.environ.clear()
    os.environ["DJANGO_SECRET_KEY"] = "test_secret_key"

@pytest.fixture
def bridge_client(environment):
    """
    Fixture to provide a test client with the X-Requested-With header.
    This causes the django_bridge middleware to return JSON
    """
    from django.test import Client
    return Client(
        headers={
            "X-Requested-With": "DjangoBridge"
        }
    )