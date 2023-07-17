from functools import wraps
from typing import Type
from starlette.requests import Request
from starlette.responses import JSONResponse

import msgspec

def parse_body_as(spec: Type[msgspec.Struct]):
    """
    Decorator. Give it a class that inherits from Struct, and it will parse the json
    body and place the parsed class as request.state.body.
    """
    def decorator(func):
        @wraps(func)
        async def inner(request: Request):
            # a JSON error occuring during parsing the body is definitely a 422.
            # but a JSON decoding error occuring elsewhere might be our fault.
            try:
                data = msgspec.json.decode(await request.body(), type=spec)
                request.state.body = data
            except (msgspec.DecodeError, msgspec.ValidationError) as e:
                return JSONResponse(status_code=422, content={"error": str(e)})
            else:
                return await func(request)
        return inner
    return decorator