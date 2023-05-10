import pytest
from sqlalchemy.pool import StaticPool
from sqlmodel import create_engine, Session, SQLModel
from v1.env import Environment
from v1.dependencies.session import get_session
from v1.models.sessions import OrchardSessionToken
from v1.models.user import User
from v1.v1_main import app
from fastapi.testclient import TestClient
from unittest.mock import patch
from v1.dependencies.tokens import get_paseto_key, session_token_to_key

from datetime import datetime, timedelta

@pytest.fixture(name="session") 
def session_fixture(): 
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session 


@pytest.fixture(name="client")  # 
def client_fixture(session: Session): 
    def get_session_override(): 
        return session

    app.dependency_overrides[get_session] = get_session_override  

    client = TestClient(app) 
    yield client 
    app.dependency_overrides.clear()


@pytest.fixture(name="user1")
def user1_fixture(session: Session):
    existing_user = User(discord_id="hello_user")
    session.add(existing_user)
    session.commit()
    return existing_user


@pytest.fixture(name="user1_token")
def user1_token_fixture(user1: User):
    session_token = OrchardSessionToken(sub=user1.discord_id, iat=datetime.now(), exp=datetime.now() + timedelta(days=14))
    key = session_token_to_key(session_token, get_paseto_key())
    return key


@pytest.fixture
def non_mocked_hosts(autouse=True) -> list:
    return ["testserver", ""]


@pytest.fixture(autouse=True)
def mock_env():
    fake_env = Environment(
        discord_client_id="MOCK_discord_client_id",
        discord_client_secret="MOCK_discord_client_secret",
        discord_bot_api_key="MOCK_discord_bot_api_key",
        paseto_key_base64="4xeS9zuI5a9YqXu4QDAE02oeQO6ZL5uvOvP9pd/Oyc0=",
        orchard_db_path="/dev/null"
    )
    with patch("v1.env._env", return_value=fake_env):
        yield