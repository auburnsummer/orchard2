"""
Discord interactions.

Generally speaking, because I have the rhythm.cafe website, I _don't_ want to have to implement
UI twice. Once in a website, and once in Discord. So, the only thing Discord interactions do
is send a link to rhythm.cafe, which does the actual work.

The format of the link is always the same. It's rhythm.cafe/interactions/<endpoint>

 - where <endpoint> is a string defined by the slash command. This is always equal to the name
 of the slash command.

There are also some query parameters that are added.

 - token: a Paseto token that contains the Discord user ID of the user who initiated the interaction.
          this is the same as a token that would be acquired via the normal login flow, so users can
          persist a new login session with it.

 - guild_token: a Paseto token that contains the Discord guild ID of the guild that the interaction,
                and the value of <endpoint>.
                basically, a guild_token for /foo cannot be used for /bar.

 - if the command is a message command, the message ID is passed as a query parameter message_id

 - any other parameters passed into the slash command are passed through to the endpoint.

The endpoint must validate both token and guild_token, and then we can do whatever we want.

"""

from fastapi import APIRouter, Request
from v1.dependencies.discord_interaction_auth import RequiresDiscordAuth
from v1.dependencies.tokens import make_user_session_token
from v1.models.discord import (
    BaseInteraction,
    DataInteraction,
    DiscordInteractionType,
    InteractionCallbackType,
    ApplicationCommandPayload,
    InteractionResponse,
    ApplicationCommandType
)

interaction_router = APIRouter()

# sometimes discord caches the DNS of the interactions endpoint, so if _we_ change IP,
# discord will still try to send the request to the old IP.
# The workaround is to have two endpoints, and switch between them when we change IP.
@interaction_router.post("/interactions")
@interaction_router.post("/interactions2")
async def interactions(request: Request, _: RequiresDiscordAuth):
    body = await request.json()
    payload = BaseInteraction(**body)
    # handle ping
    if payload.type == DiscordInteractionType.PING:
        return InteractionResponse(type=InteractionCallbackType.PONG)
    # if we're here it must have data.
    if payload.type == DiscordInteractionType.APPLICATION_COMMAND:
        data = DataInteraction(**body)
        command_payload = ApplicationCommandPayload(**data.data)
        interaction_name = command_payload.name
        user = make_user_session_token()
        options = command_payload.options
        query_params = {}