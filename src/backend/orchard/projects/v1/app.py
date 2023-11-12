from orchard.projects.v1.routes.users import logout_handler, me_handler
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from .models.engine import lifespan




async def homepage(request):
    return JSONResponse({'hello': 'world'})

routes = [
    Route("/", endpoint=homepage, methods=["GET", "POST"]),
    Route("/user/me", endpoint=me_handler, methods=["GET"]),
    Route("/user/logout", endpoint=logout_handler, methods=["POST"]),

    # Route("/auth/token/discord", endpoint=discord_token_handler, methods=["POST"]),

    # Route("/level/prefill", endpoint=prefill_handler, methods=["POST"]),

    # # sometimes discord caches the dns incorrectly, changing the url helps.
    # Route("/discord_interactions", endpoint=interaction_handler, methods=["POST"]),
    # Route("/discord_interactions2", endpoint=interaction_handler, methods=["POST"]),

    # Route("/admin/update_interactions", endpoint=update_slash_commands_handler, methods=["POST"]),

    # Route("/publisher/new/discord", endpoint=create_new_publisher_via_discord_guild_handler, methods=["POST"]),
    # Route("/publisher/identify", endpoint=get_publisher_handler, methods=["GET"])
]

app = Starlette(
    debug=True,
    routes=routes,
    lifespan=lifespan,
    middleware=[
        Middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*']),
    ]
)