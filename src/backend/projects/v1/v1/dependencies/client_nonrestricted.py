"""
A httpx client that is not rate-limited.

Used for calling API endpoints which are assumed to not have rate limits.
"""
from typing import Annotated, TypeAlias
from fastapi import Depends
import httpx

client = httpx.AsyncClient()


async def client_nonrestricted_shutdown():
    await client.aclose()


async def client_nonrestricted():
    return client

ClientNonrestricted: TypeAlias = Annotated[httpx.AsyncClient, Depends(client_nonrestricted)]