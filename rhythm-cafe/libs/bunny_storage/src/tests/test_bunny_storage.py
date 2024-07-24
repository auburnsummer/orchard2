from io import BytesIO
from httpx import AsyncClient, MockTransport, Response
import pytest

from bunny_storage import BunnyStorage
from utils.hash import sha1

@pytest.fixture
def mock_client():
    def handler():
        return Response(200, json={"text": "Hello, world!"})

    return AsyncClient(
        transport=MockTransport(handler)
    )

@pytest.fixture
def mock_bunny(mock_client):
    return BunnyStorage(
        "mock_api_key",
        "https://mock_api.bunny.invalid",
        "mock_storage_zone",
        "https://mock_cdn.bunny.invalid",
        mock_client
    )

@pytest.fixture
def mock_file():
    return BytesIO(b"abcdefghijklmnopqrstuvwxyz")

@pytest.fixture
def mock_file_hash():
    return "32d10c7b8cf96570ca04ce37f2a19d84240d3a89"

def test_mock_file(mock_file, mock_file_hash):
    assert mock_file_hash == sha1(mock_file)

def test_build_path(mock_bunny: BunnyStorage):
    assert mock_bunny._build_path("/rdzips/av/av", "aaa.rdzip") == "https://mock_api.bunny.invalid/mock_storage_zone/rdzips/av/av/aaa.rdzip"

def test_get_hash_parts(mock_bunny: BunnyStorage, mock_file):
    assert mock_bunny._get_hash_parts(mock_file) == ("32", "d1", "0c7b8cf96570ca04ce37f2a19d84240d3a89")

def test_get_hash_path_and_file_name(mock_bunny: BunnyStorage, mock_file):
    assert mock_bunny._get_hash_path_and_file_name(mock_file, "rdzips", ".rdzip") == ("rdzips/32/d1", "0c7b8cf96570ca04ce37f2a19d84240d3a89.rdzip")

def test_get_public_url(mock_bunny: BunnyStorage):
    assert mock_bunny.get_public_url("https://mock_api.bunny.invalid/mock_storage_zone/rdzips/av/av/aaa.rdzip") == "https://mock_cdn.bunny.invalid/rdzips/av/av/aaa.rdzip"