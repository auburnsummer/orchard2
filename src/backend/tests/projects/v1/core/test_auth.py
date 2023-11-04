from datetime import timedelta
from orchard.projects.v1.core.exceptions import AuthorizationHeaderInvalid, AuthorizationHeaderTokenTypeIsNotBearer, MissingAuthorizationHeader, NoAuthorizationHeaderTokenType
import pyseto
import pytest
import random

from orchard.projects.v1.core.auth import OrchardAuthScopes, PublisherAddScope, parse_token_from_request, make_token_now
from starlette.requests import Request
from starlette.datastructures import Headers

from unittest.mock import patch

# https://stackoverflow.com/a/67513232/15242232
def build_request(
    method: str = "GET",
    server: str = "www.example.com",
    path: str = "/",
    headers: dict = None,
    body: str = None,
) -> Request:
    if headers is None:
        headers = {}
    request = Request(
        {
            "type": "http",
            "path": path,
            "headers": Headers(headers).raw,
            "http_version": "1.1",
            "method": method,
            "scheme": "https",
            "client": ("127.0.0.1", 8080),
            "server": (server, 443),
        }
    )
    if body:

        async def request_body():
            return body

        request.body = request_body
    return request


def test_parse_token_from_request_throws_missing_authorization_header_when_there_is_none():
    request = build_request()
    with pytest.raises(MissingAuthorizationHeader):
        _ = parse_token_from_request(request)


def test_parse_token_from_request_throws_no_token_type():
    request = build_request(headers={
        "Authorization": "blahblahblah"
    })
    with pytest.raises(NoAuthorizationHeaderTokenType):
        _ = parse_token_from_request(request)


def test_parse_token_from_request_throws_on_non_bearer():
    request = build_request(headers={
        "Authorization": "Basic aewfaweklfjkalwejflkawefwe"
    })
    with pytest.raises(AuthorizationHeaderTokenTypeIsNotBearer):
        _ = parse_token_from_request(request)


def test_parse_token_from_request_throws_on_invalid_token():
    with patch("orchard.projects.v1.core.auth.paseto_key", new=pyseto.Key.new(version=4, purpose="local", key=random.randbytes(32))):
        token = make_token_now(OrchardAuthScopes(Admin_all=True), timedelta(hours=5))

    request = build_request(headers={
        "Authorization": f"Bearer {token}"
    })
    with pytest.raises(AuthorizationHeaderInvalid):
        _ = parse_token_from_request(request)


def test_parse_token_from_request():
    token = make_token_now(OrchardAuthScopes(Admin_all=True), timedelta(hours=5))
    request = build_request(headers={
        "Authorization": f"Bearer {token}"
    })
    parsed = parse_token_from_request(request)
    assert parsed.Admin_all == True

def test_parse_token_from_request_combines_comma_seperated_tokens():
    token = make_token_now(OrchardAuthScopes(User_all="yuki"), timedelta(hours=5))
    token2 = make_token_now(
        OrchardAuthScopes(
            Publisher_add=PublisherAddScope(
                publisher_id="testid",
                url="https://example.com/example.rdzip",
                user_id="testuser"
            )
        ), timedelta(hours=5)
    )
    request = build_request(headers={
        "Authorization": f"Bearer {token},Bearer {token2}"
    })
    parsed = parse_token_from_request(request)
    assert parsed.User_all == "yuki"
    assert parsed.Publisher_add == PublisherAddScope(
        publisher_id="testid",
        url="https://example.com/example.rdzip",
        user_id="testuser"
    )

