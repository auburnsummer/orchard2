from typing import Any, BinaryIO

from tenacity import retry, stop_after_attempt
from utils.hash import sha256, sha1

from loguru import logger

BUF_SIZE = 65536  # lets read stuff in 64kb chunks!


from http import HTTPStatus

from aiohttp_s3_client import S3Client

async def io_to_generator(f: BinaryIO):
    f.seek(0)
    while True:
        data = f.read(BUF_SIZE)
        if not data:
            return 
        yield data

DRINKS = {
    "a": "americano",
    "b": "boba",
    "c": "chai",
    "d": "darjeeling",
    "e": "earlgrey",
    "f": "flatwhite",
    "0": "ginseng",
    "1": "hotchocolate",
    "2": "icecream",
    "3": "jasmine",
    "4": "kombucha",
    "5": "lemonade",
    "6": "matcha",
    "7": "nutmeg",
    "8": "oolong",
    "9": "pumpkinspice"
}

def get_hash_parts(file: BinaryIO):
    "For the hash directory structure, the hash is first, next 2, then the rest"
    file_hash = sha1(file)
    dir1, dir2, rest = DRINKS[file_hash[0:1]], file_hash[1:3], file_hash[3:]
    return dir1, dir2, rest

def get_path(file: BinaryIO, namespace: str, file_extension: str):
    dir1, dir2, rest = get_hash_parts(file)
    file_name = f"{rest}.{file_extension.lstrip('.')}"
    path = f"{namespace}/{dir1}/{dir2}"
    return f"{path}/{file_name}"


class Essfree:
    client: S3Client
    public_cdn_base: str

    def __init__(self, client: S3Client, public_cdn_base: str):
        self.client = client
        self.public_cdn_base = public_cdn_base

    async def file_exists(self, path: str):
        try:
            async with self.client.head(path) as resp:
                if resp.status != HTTPStatus.OK:
                    return False
                return True
        except Exception:
            return False

    @retry(stop=stop_after_attempt(2))
    async def upload_file(self, file: BinaryIO, namespace: str, file_extension: str):
        path = get_path(file, namespace, file_extension)
        if await self.file_exists(path):
            logger.info(f"File {path} already exists, therefore skipping upload")
            return self.get_public_url(path)
        file.seek(0, 2)
        data_length=file.tell()
        file.seek(0)
        async with self.client.put(
            path,
            io_to_generator(file),
            data_length=data_length
        ) as resp:
            if resp.status != HTTPStatus.OK:
                raise Exception(f"Failed to upload file to S3: {resp.status}")  
        logger.info(f"Uploaded file to S3: {path}")
        return self.get_public_url(path)
            
    def get_public_url(self, path: str):
        return f"{self.public_cdn_base}/{path}"