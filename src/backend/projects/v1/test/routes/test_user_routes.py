from fastapi.testclient import TestClient
from sqlmodel import Session
from v1.dependencies.tokens import get_paseto_key, session_token_to_key
from v1.models.sessions import OrchardSessionToken
from v1.models.user import User

from v1.v1_main import app as v1_app
from datetime import datetime, timedelta


def test_post_user_create_creates_a_user(client: TestClient):
    session_token = OrchardSessionToken(sub="hello_user", iat=datetime.now(), exp=datetime.now() + timedelta(days=14))
    key = session_token_to_key(session_token, get_paseto_key())
    client = TestClient(v1_app)
    resp = client.post("/user/create", headers={
        "authorization": f"Bearer {key}"
    })
    assert resp.status_code == 201
    parsed = User(**resp.json())
    assert parsed == User(discord_id="hello_user", logout_time=datetime.fromtimestamp(0))
 

def test_post_user_create_returns_409_if_user_already_exists(session: Session, client: TestClient, user1_token: str):
    client = TestClient(v1_app)
    resp = client.post("/user/create", headers={
        "authorization": f"Bearer {user1_token}"
    })
    assert resp.status_code == 409