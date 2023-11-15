from datetime import timedelta, datetime, timezone
from httpx import AsyncClient
from orchard.projects.v1.core.auth import OrchardAuthScopes, make_token_now
from orchard.projects.v1.models.engine import select, update
from orchard.projects.v1.models.users import User

# from orchard.projects.v1.models.users import EditUser, add_user, update_user, get_user_by_id

import pytest

@pytest.mark.asyncio
async def test_homepage(client: AsyncClient):
    response = await client.get('/')
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_user_me(client: AsyncClient):
    user = User.create("mafuyu")
    token = make_token_now(OrchardAuthScopes(User_all=user.id), timedelta(hours=5))
    response = await client.get('/user/me', headers={
        "Authorization": f"Bearer {token}"
    })
    response.raise_for_status()
    assert response.status_code == 200
    assert response.json() == {
        "name": "mafuyu",
        "id": user.id,
        "cutoff": "1970-01-01T00:00:00Z",
        "avatar_url": None
    }

@pytest.mark.asyncio
async def test_user_me_returns_401_on_non_existant_user(client: AsyncClient):
    token = make_token_now(OrchardAuthScopes(User_all="abc"), timedelta(hours=5))
    response = await client.get('/user/me', headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 401
    assert response.json() == {
        "error_code": "UserDoesNotExist",
        "message": "User with id abc does not exist.",
        "extra_data": {
            "user_id": "abc"
        }
    }


@pytest.mark.asyncio
async def test_user_me_returns_401_on_expired_token(client: AsyncClient):
    user = User.create(name="mafuyu")
    id = user.id
    token = make_token_now(OrchardAuthScopes(User_all=id), timedelta(hours=-5))
    response = await client.get('/user/me', headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 401
    assert response.json() == {
        "error_code": "AuthorizationHeaderInvalid",
        "message": "Token expired."
    }

@pytest.mark.asyncio
async def test_user_me_returns_403_on_token_without_user_scope(client: AsyncClient):
    token = make_token_now(OrchardAuthScopes(), timedelta(hours=5))
    response = await client.get('/user/me', headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 403
    assert response.json() == {
        'error_code': 'MissingScopes',
        'message': 'Token lacks the required scope: User_all',
        'extra_data': {
            'scope': 'User_all'
        }
    }

@pytest.mark.asyncio
async def test_user_me_returns_403_on_token_issued_before_cutoff(client: AsyncClient):
    user = User.create(name="mafuyu")
    id = user.id
    # user = await update_user(id, EditUser(cutoff=datetime(2016, 6, 2)))
    user.cutoff = datetime(2016, 6, 2).astimezone(timezone.utc)
    update(user)
    # now is 2016-01-01
    token = make_token_now(OrchardAuthScopes(User_all=id), timedelta(hours=5))
    response = await client.get('/user/me', headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 403
    assert response.json() == {
        "error_code": "UserIsLoggedOut",
        "message": f"User with id {user.id} is logged out.",
        "extra_data": {
            "user_id": user.id
        }
    }

@pytest.mark.asyncio
async def test_user_logout_sets_cutoff_date(client: AsyncClient):
    user = User.create(name="mafuyu")
    id = user.id
    assert user.cutoff == datetime(1970, 1, 1, tzinfo=timezone.utc)
    token = make_token_now(OrchardAuthScopes(User_all=id), timedelta(hours=5))
    response = await client.post('/user/logout', headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 204
    user2 = select(User).by_id(id)
    # 2016/01/01 started when the tests started
    # so this is a few milliseconds ahead
    assert user2.cutoff >= datetime(2016, 6, 1, tzinfo=timezone.utc)