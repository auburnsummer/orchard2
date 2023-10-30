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

from .routes.interactions.route import interaction_handler

from .routes.admin import (
    update_slash_commands_handler
)

from .routes.publishers import (
    create_new_publisher_via_discord_guild_handler,
    get_publisher_handler
)


async def homepage(request):
    return JSONResponse({'hello': 'world'})

routes = [
    Route("/", endpoint=homepage, methods=["GET", "POST"]),
    Route("/user/me", endpoint=me_handler, methods=["GET"]),
    Route("/user/logout", endpoint=logout_handler, methods=["POST"]),

    Route("/auth/token/discord", endpoint=discord_token_handler, methods=["POST"]),

    Route("/level/prefill", endpoint=prefill_handler, methods=["POST"]),

    # sometimes discord caches the dns incorrectly, changing the url helps.
    Route("/discord_interactions", endpoint=interaction_handler, methods=["POST"]),
    Route("/discord_interactions2", endpoint=interaction_handler, methods=["POST"]),

    Route("/admin/update_interactions", endpoint=update_slash_commands_handler, methods=["POST"]),

    Route("/publisher/new/discord", endpoint=create_new_publisher_via_discord_guild_handler, methods=["POST"]),
    Route("/publisher/identify", endpoint=get_publisher_handler, methods=["GET"])
]

app = Starlette(
    debug=True,
    routes=routes,
    lifespan=lifespan,
    middleware=[
        Middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*']),
    ]
)