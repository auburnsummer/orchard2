from io import BytesIO
from os import strerror
from httpx import AsyncClient


def sha256(f: BytesIO) -> str:
    pass

class BunnyStorage:
    api_key: str
    base_endpoint: str
    storage_zone_name: str
    client: AsyncClient

    def __init__(self, api_key: str, base_endpoint: str, storage_zone_name: str):
        self.api_key = api_key
        self.base_endpoint = base_endpoint
        self.storage_zone_name = storage_zone_name
        self.client = AsyncClient()

    def _build_path(self, path: str, file_name: str):
        stripped_path = path.lstrip("/") 
        return f"https://{self.base_endpoint}/{self.storage_zone_name}/{stripped_path}/{file_name}"

    def _build_headers(self):
        return {
            "AccessKey": self.api_key
        }

    

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.client.aclose()
