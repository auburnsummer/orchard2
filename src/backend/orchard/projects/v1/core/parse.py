

import json
from pydantic import BaseModel
from functools import wraps
from typing import Type
from starlette.requests import Request
from starlette.responses import JSONResponse


def parse_body_as(pydantic_class: Type[BaseModel]):
    """
    Decorator. Give it a class that inherits from BaseModel, and it will parse the json
    body and place the parsed class as request.state.body.
    """
    def decorator(func):
        @wraps(func)
        async def inner(request: Request):
            # a JSON error occuring during parsing the body is definitely a 422.
            # but a JSON decoding error occuring elsewhere might be our fault.
            try:
                data = pydantic_class(**await request.json())
                request.state.body = data
                return await func(request)
            except json.JSONDecodeError as e:
                return JSONResponse(status_code=422, content={"error": str(e)})
            except TypeError as e:
                return JSONResponse(status_code=422, content={"error": "Body was not a mapping."})
        return inner
    return decorator