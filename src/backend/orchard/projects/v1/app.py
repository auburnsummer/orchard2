from orchard.projects.v1.routes.levels import prefill_handler
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from .models.metadata import lifespan

from .routes.users import (
    me_handler,
    logout_handler
)

from .routes.discord_auth import (
    discord_token_handler
)


async def homepage(request):
    return JSONResponse({'hello': 'world'})

routes = [
    Route("/", endpoint=homepage, methods=["GET", "POST"]),
    Route("/user/me", endpoint=me_handler, methods=["GET"]),
    Route("/user/logout", endpoint=logout_handler, methods=["POST"]),

    Route("/auth/token/discord", endpoint=discord_token_handler, methods=["POST"]),

    Route("/level/prefill", endpoint=prefill_handler, methods=["POST"])
]

app = Starlette(
    debug=True,
    routes=routes,
    lifespan=lifespan,
    middleware=[
        Middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*']),
    ]
)