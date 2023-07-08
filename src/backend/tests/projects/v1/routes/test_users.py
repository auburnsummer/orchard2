from datetime import timedelta, datetime
from httpx import AsyncClient
from orchard.projects.v1.core.auth import OrchardAuthScopes, make_token_now

from orchard.projects.v1.models.users import EditUser, add_user, update_user, get_user_by_id

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
    response = await client.get('/user/me', headers={
        "Authorization": f"Bearer {token}"
    })
    response.raise_for_status()
    assert response.status_code == 200
    assert response.json() == {
        "name": "mafuyu",
        "id": id,
        "cutoff": "1970-01-01T00:00:00",
        "avatar_url": None
    }


@pytest.mark.asyncio
async def test_user_me_returns_401_on_expired_token(client: AsyncClient):
    user = await add_user(name="mafuyu")
    id = user.id
    token = make_token_now(OrchardAuthScopes(user=id), timedelta(hours=-5))
    response = await client.get('/user/me', headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 401
    assert response.json() == {'error': 'Token expired.'}


@pytest.mark.asyncio
async def test_user_me_returns_401_on_token_without_user_scope(client: AsyncClient):
    token = make_token_now(OrchardAuthScopes(), timedelta(hours=5))
    response = await client.get('/user/me', headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 401
    assert response.json() == {'error': 'Token lacks the required scope: user'}


@pytest.mark.asyncio
async def test_user_me_returns_401_on_token_issued_before_cutoff(client: AsyncClient):
    user = await add_user(name="mafuyu")
    id = user.id
    user = await update_user(id, EditUser(cutoff=datetime(2016, 6, 2)))
    # now is 2016-01-01
    token = make_token_now(OrchardAuthScopes(user=id), timedelta(hours=5))
    response = await client.get('/user/me', headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 401
    assert response.json() == {
        "error": f"user with id {id} has been logged out."
    }


@pytest.mark.asyncio
async def test_user_logout_sets_cutoff_date(client: AsyncClient):
    user = await add_user(name="mafuyu")
    id = user.id
    assert user.cutoff == datetime(1970, 1, 1)
    token = make_token_now(OrchardAuthScopes(user=id), timedelta(hours=5))
    response = await client.post('/user/logout', headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 204
    user = await get_user_by_id(id)
    assert user.cutoff == datetime(2016, 6, 1)