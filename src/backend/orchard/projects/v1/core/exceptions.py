"""
Any user-facing exception lives here. Exceptions have:

 - an associated HTTP status code. We currently assume this is static.
 - a string message which is user-readable.
 - an optional struct extra_data which contains any extra info.

When an exception is raised anywhere in a request, if it's not handled explicitly
within the request, it'll bubble up to msgspec_return, which will read the exception
and generate an appropriate response.
"""

import msgspec
import traceback
from typing import Set, TypedDict
from typing_extensions import Unpack


class OrchardException(Exception):
    status_code: int
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.status_code = 500
    
    def extra_data(self):
        return None


class JustAMessage(TypedDict):
    """
    Some exceptions just have a custom string without any other structured data, this type is for that.
    """
    message: str


class MissingAuthorizationHeader(OrchardException):
    """
    Thrown when an endpoint requires an Authorization header but an Authorization header was not provided.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.status_code = 401

    def __str__(self):
        return "No Authorization header."


class NoAuthorizationHeaderTokenType(OrchardException):
    """
    Thrown when an endpoint requires an Authorization header but the header was not able to be parsed into a token type and token.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.status_code = 401

    def __str__(self):
        return "No token type in the header."


class AuthorizationHeaderTokenTypeIsNotBearer(OrchardException):
    """
    Thrown when an endpoint requires a Bearer token but a different token type was provided.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.status_code = 401

    def __str__(self):
        return "Token type should be Bearer."


class AuthorizationHeaderInvalid(OrchardException):
    """
    Thrown when an endpoint requires a Bearer token but the token is malformed or signed with the wrong key, etc.
    """
    def __init__(self, *args, **kwargs: Unpack[JustAMessage]):
        super().__init__(*args)
        self.message = kwargs.get("message")
        self.status_code = 401
    
    def __str__(self):
        return self.message


class MissingScopesArgs(TypedDict):
    scope: str


class MissingScopesExtraData(msgspec.Struct):
    scope: str


class MissingScopes(OrchardException):
    """
    Thrown when an endpoint requires certain authorization scopes, but the provided token does not have those scopes.
    """
    def __init__(self, *args, **kwargs: Unpack[MissingScopesArgs]):
        super().__init__(*args)
        self.scope = kwargs.get('scope')
        self.status_code = 403

    def __str__(self):
        return f"Token lacks the required scope: {self.scope}"

    def extra_data(self):
        return MissingScopesExtraData(scope=self.scope)


class UserDoesNotExistArgs(TypedDict):
    user_id: str

class UserDoesNotExistExtraData(msgspec.Struct):
    user_id: str

class UserDoesNotExist(OrchardException):
    """
    Thrown when a user does not exist
    """
    def __init__(self, *args, **kwargs: Unpack[UserDoesNotExistArgs]):
        super().__init__(*args)
        self.user_id = kwargs.get("user_id")
        self.status_code = 401

    def __str__(self):
        return f"User with id {self.user_id} does not exist."

    def extra_data(self):
        return UserDoesNotExistExtraData(user_id=self.user_id)

class PublisherDoesNotExistArgs(TypedDict):
    publisher_id: str

class PublisherDoesNotExistExtraData(msgspec.Struct):
    publisher_id: str

class PublisherDoesNotExist(OrchardException):
    """
    Thrown when a publisher does not exist
    """
    def __init__(self, *args, **kwargs: Unpack[PublisherDoesNotExistArgs]):
        super().__init__(*args)
        self.publisher_id = kwargs.get("publisher_id")
        self.status_code = 401

    def __str__(self):
        return f"User with id {self.publisher_id} does not exist."

    def extra_data(self):
        return PublisherDoesNotExistExtraData(publisher_id=self.publisher_id)
    

class MissingDiscordSignatureHeaders(OrchardException):
    """
    Thrown on the interactions endpoint if the headers are missing.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.status_code = 401
    
    def __str__(self):
        return f"Missing required Discord headers."


class InvalidDiscordSignature(OrchardException):
    """
    Thrown on the interactions endpoint if the headers are invalid.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.status_code = 401
    
    def __str__(self):
        return f"Invalid request signature."

class UserIsLoggedOutArgs(TypedDict):
    user_id: str

class UserIsLoggedOutExtraData(msgspec.Struct):
    user_id: str

class UserIsLoggedOut(OrchardException):
    """
    Thrown when authentication token is expired, typically because user is logged out.
    """
    def __init__(self, *args, **kwargs: Unpack[UserIsLoggedOutArgs]):
        super().__init__(*args)
        self.user_id = kwargs.get("user_id")
        self.status_code = 403
    
    def __str__(self):
        return f"User with id {self.user_id} is logged out."

    def extra_data(self):
        return UserIsLoggedOutExtraData(user_id=self.user_id)


class BodyValidationError(OrchardException):
    """
    Thrown when the request body could not be parsed or did not have the correct form.
    """
    def __init__(self, *args, **kwargs: Unpack[JustAMessage]):
        super().__init__(*args)
        self.message = kwargs.get("message")
        self.status_code = 422

    def __str__(self):
        return self.message


class NotAdmin(OrchardException):
    """
    Thrown if a non-admin token is used on an admin endpoint.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
    
    def __str__(self):
        return "Not admin"

class DiscordCredentialNotFoundArgs(TypedDict):
    credential_id: str

class DiscordCredentialNotFoundExtraData(msgspec.Struct):
    pass

class DiscordGuildCredentialAlreadyExistsArgs(TypedDict):
    credential_id: str

class DiscordGuildCredentialAlreadyExistsExtraData(msgspec.Struct):
    credential_id: str

class DiscordGuildCredentialAlreadyExists(OrchardException):
    def __init__(self, *args, **kwargs: Unpack[DiscordGuildCredentialAlreadyExistsArgs]):
        super().__init__(*args)
        self.credential_id = kwargs.get('credential_id')
        self.status_code = 409
    
    def __str__(self):
        return f"Discord guild credential {self.credential_id} already is linked to a publisher."

    def extra_data(self):
        return DiscordGuildCredentialAlreadyExistsExtraData(
            credential_id=self.credential_id
        )

class LinkedTokensIDMismatchArgs(TypedDict):
    id1: str
    id2: str
    context: str

class LinkedTokensIDMismatch(OrchardException):
    def __init__(self, *args, **kwargs: Unpack[LinkedTokensIDMismatchArgs]):
        super().__init__(*args)
        self.id1 = kwargs.get('id1')
        self.id2 = kwargs.get('id2')
        self.context = kwargs.get('context')
        self.status_code = 403
    
    def __str__(self):
        return f"{self.context}: received mismatching ids {self.id1} and {self.id2}. Try the command from the start. If you see this again, it's a bug, ping auburn"


class UnknownErrorArgs(TypedDict):
    orig_exc: Exception

class UnknownError(OrchardException):
    def __init__(self, *args, **kwargs: Unpack[UnknownErrorArgs]):
        super().__init__(*args)
        self.orig_exc = kwargs.get('orig_exc')
        self.status_code = 500

    def __str__(self):
        error_str = '\n'.join(traceback.format_exception_only(self.orig_exc))
        return f"Unhandled error: {error_str}"