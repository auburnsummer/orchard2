from io import BytesIO
from os import strerror
from typing import BinaryIO, Optional
from httpx import AsyncClient, HTTPStatusError

from utils.hash import sha256, sha1
from tenacity import retry, wait_exponential, stop_after_attempt

from loguru import logger

BUF_SIZE = 65536  # lets read stuff in 64kb chunks!


def io_to_generator(f: BinaryIO):
    f.seek(0)
    while True:
        data = f.read(BUF_SIZE)
        if not data:
            return 
        yield data


class BunnyStorage:
    api_key: str
    base_endpoint: str
    storage_zone_name: str
    public_cdn_base: str
    client: AsyncClient

    def __init__(
            self,
            api_key: str,
            base_endpoint: str,
            storage_zone_name: str,
            public_cdn_base: str,
            client: AsyncClient
        ):
        """
        Initialize the BunnyStorage object. This should always be used as part of a
        context manager, e.g.:

        async with httpx.AsyncClient() as client:
            storage = BunnyStorage(...)
        """
        self.api_key = api_key
        self.base_endpoint = base_endpoint
        self.storage_zone_name = storage_zone_name
        self.client = client
        self.public_cdn_base = public_cdn_base

    def _build_path(self, path: str, file_name: str):
        "Build valid bunny URL from a partial path"
        stripped_path = path.lstrip("/") 
        return f"{self.base_endpoint}/{self.storage_zone_name}/{stripped_path}/{file_name}"

    def _get_hash_parts(self, file: BinaryIO):
        "For the hash directory structure, the hash is first 2, next 2, then the rest"
        file_hash = sha1(file)
        dir1, dir2, rest = file_hash[0:2], file_hash[2:4], file_hash[4:]
        return dir1, dir2, rest

    def _get_hash_path_and_file_name(self, file: BinaryIO, namespace: str, file_extension: str):
        "For the hash directory structure, we have namespaces at the top level as well, plus filenames"
        dir1, dir2, rest = self._get_hash_parts(file)
        path = f"{namespace}/{dir1}/{dir2}"
        file_name = f"{rest}.{file_extension.lstrip('.')}"
        return path, file_name

    def get_url_by_hash(self, file: BinaryIO, namespace: str, file_extension: str):
        path, file_name = self._get_hash_path_and_file_name(file, namespace, file_extension)
        return self._build_path(path, file_name)

    def get_public_url(self, private_url: str):
        return private_url.replace(f"{self.base_endpoint}/{self.storage_zone_name}", self.public_cdn_base)

    async def file_exists(self, path: str, file_name: str):
        url = self._build_path(path, file_name)
        resp = await self.client.get(url, headers={
            "AccessKey": self.api_key,
            "Range": "bytes=0-1"
        })
        try:
            resp.raise_for_status()
            return True
        except HTTPStatusError:
            return False

    @retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(2), reraise=True)
    async def upload_file(self, file: BinaryIO, path: str, file_name: str, skip_if_already_exists: bool):
        if skip_if_already_exists:
            already_exists = await self.file_exists(path, file_name)
            if already_exists:
                logger.info(f"Skipping upload of {path}/{file_name} as it already exists.")
                return
        url = self._build_path(path, file_name)
        file_hash = sha256(file).upper()
        await self.client.put(url, headers={
            "AccessKey": self.api_key,
            "Checksum": file_hash
        }, content=io_to_generator(file))

    async def upload_file_by_hash(self, file: BinaryIO, namespace: str, file_extension: str):
        path, file_name = self._get_hash_path_and_file_name(file, namespace, file_extension)

        await self.upload_file(file, path, file_name, True)
        return self.get_url_by_hash(file, namespace, file_extension)