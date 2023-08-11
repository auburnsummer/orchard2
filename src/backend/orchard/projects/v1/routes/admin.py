"""
THE ADMIN ROUTES

These require an admin-scoped token and are related to maintenance tasks of orchard itself.

from orchard.projects.v1.core.auth import *
token = make_token_now(OrchardAuthScopes(admin=True), timedelta(days=1))
"""
from functools import wraps
from orchard.projects.v1.core.config import config
from orchard.projects.v1.core.exceptions import NotAdmin
from orchard.projects.v1.core.forward import forward_httpx
from orchard.projects.v1.routes.interactions.commands import ALL_COMMANDS
from starlette.requests import Request

from orchard.projects.v1.core.auth import OrchardAuthToken, requires_scopes
from orchard.projects.v1.core.wrapper import msgspec_return, parse_body_as

from typing import Optional

import msgspec
import httpx

def requires_admin(func):
    @wraps(func)
    @requires_scopes({"admin"})
    async def inner(request: Request):
        token: OrchardAuthToken = request.state.token

        assert token.admin is not None

        if token.admin:
            return await func(request)
        else:
            return NotAdmin()
    return inner


class UpdateSlashCommandsHandlerArgs(msgspec.Struct):
    guild_id: Optional[str] = None  # if None, we're updating globally.

@msgspec_return
@parse_body_as(UpdateSlashCommandsHandlerArgs)
@requires_admin
async def update_slash_commands_handler(request: Request):
    """
    Update the slash commands definitions.

    In the future, it would be better to have this be automatic based on CI when
    the relevant files change (i.e. anything in orchard/projects/v1/interactions)
    """
    args: UpdateSlashCommandsHandlerArgs = request.state.body

    c = config()

    if args.guild_id is None:
        url = f"https://discord.com/api/v10/applications/{c.DISCORD_APPLICATION_ID}/commands"
    else:
        url = f"https://discord.com/api/v10/applications/{c.DISCORD_APPLICATION_ID}/guilds/{args.guild_id}/commands"

    payload = msgspec.json.encode(ALL_COMMANDS)
    async with httpx.AsyncClient() as client:
        resp = await client.put(url=url, content=payload, headers={
            "Authorization": f"Bot {c.DISCORD_BOT_TOKEN.get_secret_value()}",
            "content-type": "application/json"
        })
        return forward_httpx(resp)
