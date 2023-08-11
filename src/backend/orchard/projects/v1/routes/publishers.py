import msgspec

from orchard.projects.v1.core.wrapper import msgspec_return, parse_body_as
from orchard.projects.v1.core.auth import requires_scopes, OrchardAuthToken

from orchard.projects.v1.models.discord_guild_credentials import make_new_publisher_with_credential
from orchard.projects.v1.models.metadata import engine

from starlette.requests import Request

class CreateNewPublisherViaDiscordGuildArgs(msgspec.Struct):
    publisher_name: str

@msgspec_return(201)
@requires_scopes({"discord_guild"})
@parse_body_as(CreateNewPublisherViaDiscordGuildArgs)
async def create_new_publisher_via_discord_guild_handler(request: Request):
    args: CreateNewPublisherViaDiscordGuildArgs = request.state.body
    token: OrchardAuthToken = request.state.token
    # requires_scopes will ensure this.
    assert token.discord_guild is not None

    async with engine.begin() as conn:
        publisher, _ = await make_new_publisher_with_credential(token.discord_guild, args.publisher_name, conn) 

    return publisher