from pydantic import ValidationError
from starlette.responses import JSONResponse

from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

class PydanticErrorMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        try:
            await self.app(scope, receive, send)
        except ValidationError as exc:
            payload = {
                "error": str(exc),
                "error_info": exc.errors()
            }
            resp = JSONResponse(status_code=HTTP_422_UNPROCESSABLE_ENTITY, content=payload)
            await resp(scope, receive, send)