"""
Discord interactions.

Generally speaking, because I have the rhythm.cafe website, I _don't_ want to have to implement
UI twice. Once in a website, and once in Discord. So, the only thing Discord interactions do
is send a link to rhythm.cafe, which does the actual work.

...with one exception, which I'll get to later.

By the way, this is how publishers work in general. So if I end up implementing another publisher
type, the links to rhythm.cafe are the same. there should be little discord specific stuff here.

The format of the link is always the same. It's rhythm.cafe/publisher/<endpoint>

 - where <endpoint> is a string defined by the slash command. This may not always be equal to the
   name of the command.

Query parameters:

 - publisher_token: a Paseto token that contains the publisher id of the publisher doing the interaction,
                and the value of <endpoint>.
                basically, a publisher_token for /foo cannot be used for /bar.

 - if the command is a message command, the message ID is passed as a query parameter message_id

 - any other parameters passed into the slash command are passed through to the endpoint.

 - an important note. there is no distinction between "admin" and "non-admin" commands. all commands
   use the same system. it's up to the guild to restrict which commands can be used by which people.

The endpoint must validate guild_token, and then we can do whatever we want.

Now, the one exception. There has to be a way to create a publisher in the first place.

The /register (create a new publisher linked to this guild) and /link (link an existing publisher to this guild)
commands are the commands that "do things" in discord and don't just link to rhythm cafe.

nb: for the initial scope, only /register is planned. 
"""

from datetime import timedelta
from re import A
from orchard.projects.v1.core.auth import OrchardAuthScopes, make_token_now
from orchard.projects.v1.core.exceptions import InvalidDiscordSignature, MissingDiscordSignatureHeaders
from orchard.projects.v1.core.wrapper import msgspec_return
from starlette.requests import Request
from orchard.projects.v1.core.config import config
from orchard import __version__
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.exceptions import InvalidSignature
from textwrap import dedent

from typing import Optional

import msgspec

from .spec import (
    EPHEMERAL,
    ApplicationCommandInteraction,
    BaseInteraction,
    InteractionMessage,
    InteractionType,
    MessageInteractionResponse,
    PongInteractionResponse
)


def version_handler(_: ApplicationCommandInteraction):
    content = dedent(f"""
        ## Bot Version

        `{__version__}`
    """)
    response = MessageInteractionResponse(
        data=InteractionMessage(
            content=content,
            flags=EPHEMERAL
        )
    )
    return response


def discord_register_handler(body: ApplicationCommandInteraction):
    scopes = OrchardAuthScopes(
        DiscordGuild_register=body.guild_id
    )
    exp_time = timedelta(hours=2)
    guild_token = make_token_now(scopes, exp_time)
    content = make_publisher_link("discord_register", guild_token=guild_token)
    response = MessageInteractionResponse(
        data=InteractionMessage(
            content=content,
            flags=EPHEMERAL
        )
    )
    return response

HANDLERS = {
    "register": discord_register_handler,
    "version": version_handler
}



def make_publisher_link(
    command_name: str,
    guild_token: Optional[str] = None,
    publisher_token: Optional[str] = None,
) -> str:
    qs = ""
    if guild_token:
        qs = qs + f"guild_token={guild_token}"
    if publisher_token:
        if qs:  # if there's already stuff there, seperator with & is needed.
            qs = qs + "&"
        qs = qs + f"publisher_token={publisher_token}"
    if qs:
        qs = "?" + qs
    link = f"{config().FRONTEND_URL}/publisher/{command_name}{qs}"
    return f"Click [here]({link}) to continue"

@msgspec_return(200)
async def interaction_handler(request: Request):
    # check the discord headers.
    headers = request.headers
    try:
        sig = headers["X-Signature-Ed25519"]
        timestamp = headers["X-Signature-Timestamp"]
    except KeyError:
        return MissingDiscordSignatureHeaders()

    public_key = config().DISCORD_PUBLIC_KEY
    verify_key = Ed25519PublicKey.from_public_bytes(bytes.fromhex(public_key))
    payload = await request.body()
    # concat bytes together
    to_verify = timestamp.encode("ascii") + payload

    try:
        verify_key.verify(bytes.fromhex(sig), to_verify)
    except InvalidSignature:
        return InvalidDiscordSignature()

    # we're past the discord auth!
    body = msgspec.json.decode(payload, type=BaseInteraction)
    # first handle PING as usual.
    if body.type == InteractionType.PING:
        return PongInteractionResponse()
    
    # application commands are likely to be 99.9% of our traffic.
    # most application commands are just handled by generating a link with tokens...
    if body.type == InteractionType.APPLICATION_COMMAND:
        body = msgspec.json.decode(payload, type=ApplicationCommandInteraction)
        # ...with the exception of /version, which is handled specially.
        if body.data.name == "version":
            content = dedent(f"""
                ## Bot Version

                `{__version__}`
            """)
            response = MessageInteractionResponse(
                data=InteractionMessage(
                    content=content,
                    flags=EPHEMERAL
                )
            )
            return response
        else:
            try:
                return HANDLERS[body.data.name](body)
            except KeyError:
                content = dedent(f"I don't know what to do with the command {body.data.name}. This is a bug, please ping auburn!")
                response = MessageInteractionResponse(
                    data=InteractionMessage(
                        content=content,
                        flags=EPHEMERAL
                    )
                )
                return response