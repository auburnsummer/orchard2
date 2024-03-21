from functools import wraps
import traceback
from typing import Optional, Type
import typing
from orchard.projects.v1.core.exceptions import BodyValidationError, OrchardException, UnknownError
from starlette.requests import Request
from starlette.responses import Response

import msgspec

from loguru import logger

from urllib.parse import parse_qs

def parse_body_as(spec: Type[msgspec.Struct]):
    """
    Decorator. Give it a class that inherits from Struct, and it will parse the json
    body and place the parsed class as request.state.body.
    """
    def decorator(func):
        @wraps(func)
        async def inner(request: Request):
            try:
                data = msgspec.json.decode(await request.body(), type=spec)
                request.state.body = data
            except (msgspec.DecodeError, msgspec.ValidationError) as e:
                raise BodyValidationError(message=str(e)) from e
            else:
                return await func(request)
        return inner
    return decorator

def is_list_type(type_: typing.Any):
    "If type is of the form List[something] or Optional[List[something]], return True, otherwise False"
    if type_ == list:
        return True
    origin = typing.get_origin(type_)
    if origin is list:
        return True

    if origin is not None:
        return any(is_list_type(a) for a in typing.get_args(type_))

    return False

def parse_qs_as(spec: Type[msgspec.Struct]):
    """
    Decorator. Give it a class that inherits from Struct, and it will parse the query
    string and place the parsed result as request.state.query.

    nb: does not support nested structures at this stage.
    """
    def decorator(func):
        @wraps(func)
        async def inner(request: Request):
            try:
                list_fields = set(field.encode_name for field in msgspec.structs.fields(spec) if is_list_type(field.type))
                # nb already doesn't have leading ?
                qs = request.url.query
                parsed = parse_qs(qs)

                # if it's a list with a single item, just make it that single item.
                for key, value in parsed.items():
                    if len(value) == 1 and key not in list_fields:
                        parsed[key] = value[0]

                data = msgspec.convert(parsed, spec, strict=False)
                request.state.query = data
            except (msgspec.DecodeError, msgspec.ValidationError) as e:
                raise BodyValidationError(message=str(e)) from e
            else:
                return await func(request)
        return inner
    return decorator


class ErrorResponseContents(msgspec.Struct, kw_only=True, omit_defaults=True):
    error_code: str
    message: str
    extra_data: Optional[msgspec.Struct] = None


def orchard_exception_response(exc: OrchardException):
    response_content = ErrorResponseContents(
        error_code=type(exc).__name__,
        message=str(exc),
        extra_data=exc.extra_data()
    )
    err_response = Response(
        status_code=exc.status_code,
        content=msgspec.json.encode(response_content),
        media_type="application/json"
    )
    return err_response


def msgspec_return(status_code: int):
    """
    Decorator. If the function returns a msgspec object, automatically turns that object
    into an appropriate response.

    If the function raises an OrchardException, automatically generate an appropriate
    response as well.

    If the function raises an unhandled exception, automatically generate a decent 500 response.

    Order: this should typically be the last decorator (i.e. at the top.)
    """
    def decorator(func):
        @wraps(func)
        async def inner(request: Request):
            try:
                orig_response = await func(request)
            except OrchardException as exc:
                return orchard_exception_response(exc)
            except Exception as exc:
                logger.exception("Unhandled error")
                # logger.error(traceback.format_exc())
                synthetic_orchard_exception = UnknownError(orig_exc=exc)
                return orchard_exception_response(synthetic_orchard_exception)
            if isinstance(orig_response, msgspec.Struct):
                new_resp = Response(
                    status_code=status_code,
                    content=msgspec.json.encode(orig_response),
                    media_type="application/json"
                )
                return new_resp
            else:
                return orig_response

        return inner
    return decorator
