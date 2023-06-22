from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.middleware import Middleware

from .models.metadata import lifespan

from .routes.users import (
    list_users_handler,
    add_user_handler
)

from .core.middleware import (
    PydanticErrorMiddleware
)

async def homepage(request):
    return JSONResponse({'hello': 'world'})

routes = [
    Route("/users", endpoint=list_users_handler, methods=["GET"]),
    Route("/users", endpoint=add_user_handler, methods=["POST"]),
]

app = Starlette(
    debug=True,
    routes=routes,
    lifespan=lifespan,
    middleware=[
        Middleware(PydanticErrorMiddleware)
    ]
)