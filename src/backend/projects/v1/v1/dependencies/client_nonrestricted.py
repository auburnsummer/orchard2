"""
A httpx client that is not rate-limited.

Used for calling API endpoints which are assumed to not have rate limits.
"""
from typing import Annotated, TypeAlias
from fastapi import Depends
import httpx

client_singleton: httpx.AsyncClient | None = None


async def client_nonrestricted_shutdown():
    global client_singleton
    if client_singleton is not None:
        await client_singleton.aclose()
        client_singleton = None


async def client_nonrestricted():
    global client_singleton
    if client_singleton is None:
        client_singleton = httpx.AsyncClient()
    return client_singleton


ClientNonrestricted: TypeAlias = Annotated[httpx.AsyncClient, Depends(client_nonrestricted)]