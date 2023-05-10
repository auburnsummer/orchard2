import datetime
import pytest
from random import randbytes
from pyseto import Key, KeyInterface, VerifyError

from freezegun import freeze_time

from v1.dependencies.injected_user import *
from v1.dependencies.tokens import session_token_to_key


@pytest.fixture
def mock_paseto_key():
    # generate 32 random bytes
    key_bytes = randbytes(32)
    key = Key.new(version=4, purpose='local', key=key_bytes)
    return key


@freeze_time("2015-01-01")
def test_injected_token_decodes_valid_token(mock_paseto_key: KeyInterface):
    payload = OrchardSessionToken(sub="1234", iat=datetime.datetime(year=2015, month=1, day=1), exp=datetime.datetime(year=2015, month=2, day=1))
    token = session_token_to_key(payload, mock_paseto_key)
    assert injected_token(f"Bearer {token}", mock_paseto_key) == payload


@freeze_time("2015-01-01")
def test_injected_token_fails_on_expired_token(mock_paseto_key: KeyInterface):
    payload = OrchardSessionToken(sub="1234", iat=datetime.datetime.fromtimestamp(0), exp=datetime.datetime(year=2014, month=11, day=30))
    token = session_token_to_key(payload, mock_paseto_key)
    with pytest.raises(VerifyError):
        _ = injected_token(f"Bearer {token}", mock_paseto_key)
