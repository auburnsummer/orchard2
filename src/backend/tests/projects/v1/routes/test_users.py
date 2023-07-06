from datetime import timedelta
from httpx import AsyncClient
from orchard.projects.v1.core.auth import OrchardAuthScopes, make_token_now

from orchard.projects.v1.models.users import add_user

import pytest

@pytest.mark.asyncio
async def test_homepage(client: AsyncClient):
    response = await client.get('/')
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_user_me(client: AsyncClient):
    user = await add_user(name="mafuyu")
    id = user.id
    token = make_token_now(OrchardAuthScopes(user=id), timedelta(hours=5))
    response = await client.get('/users/me', headers={
        "Authorization": f"Bearer {token}"
    })
    response.raise_for_status()
    assert response.status_code == 200
    assert response.json() == {
        "name": "mafuyu",
        "id": id
    }


@pytest.mark.asyncio
async def test_user_me_returns_401_on_expired_token(client: AsyncClient):
    user = await add_user(name="mafuyu")
    id = user.id
    token = make_token_now(OrchardAuthScopes(user=id), timedelta(hours=-5))
    response = await client.get('/users/me', headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 401
    assert response.json() == {'error': 'Token expired.'}


@pytest.mark.asyncio
async def test_user_me_returns_401_on_token_without_user_scope(client: AsyncClient):
    token = make_token_now(OrchardAuthScopes(), timedelta(hours=5))
    response = await client.get('/users/me', headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 401
    assert response.json() == {'error': 'Token lacks the required scope: user'}


