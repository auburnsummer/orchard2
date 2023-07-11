from io import BytesIO
from os import strerror
from typing import BinaryIO
from httpx import AsyncClient
import hashlib

BUF_SIZE = 65536  # lets read stuff in 64kb chunks!


def sha256(f: BinaryIO) -> str:
    m = hashlib.sha256()
    f.seek(0)
    while True:
        data = f.read(BUF_SIZE)
        if not data:
            break
        m.update(data)
    return m.hexdigest()



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

    async def upload_file(self, file: BinaryIO, path: str, file_name: str):
        url = self._build_path(path, file_name)
        file_hash = sha256(file)
    

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.client.aclose()
