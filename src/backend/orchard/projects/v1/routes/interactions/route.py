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
from orchard.projects.v1.core.auth import OrchardAuthScopes, PublisherAddScope, make_token_now
from orchard.projects.v1.core.exceptions import InvalidDiscordSignature, MissingDiscordSignatureHeaders
from orchard.projects.v1.core.wrapper import msgspec_return
from orchard.projects.v1.models.discord_guild_credentials import get_disc_guild_credential, DiscordGuildCredentialNotFoundException
from orchard.projects.v1.models.metadata import engine
from orchard.projects.v1.models.publishers import get_publisher_by_discord_guild_credential
from starlette.requests import Request
from orchard.projects.v1.core.config import config
from orchard import __version__
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.exceptions import InvalidSignature
from textwrap import dedent

from typing import Optional, List

import msgspec

from .spec import (
    EPHEMERAL,
    AnyInteraction,
    ApplicationCommandInteraction,
    DiscordAttachment,
    InteractionMessage,
    InteractionType,
    MessageApplicationCommandData,
    MessageInteractionResponse,
    PingInteraction,
    PongInteractionResponse,
)

from loguru import logger

async def version_handler(_: ApplicationCommandInteraction):
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

async def discord_register_handler(body: ApplicationCommandInteraction):
    scopes = OrchardAuthScopes(
        DiscordGuild_register=body.guild_id
    )
    exp_time = timedelta(hours=2)
    guild_token = make_token_now(scopes, exp_time)
    content = make_publisher_link_continue("discord_register", guild_token=guild_token)
    response = MessageInteractionResponse(
        data=InteractionMessage(
            content=content,
            flags=EPHEMERAL
        )
    )
    return response


async def add_handler(body: ApplicationCommandInteraction):
    # add should always be on a message.
    if not isinstance(body.data, MessageApplicationCommandData):
        response = MessageInteractionResponse(
            data=InteractionMessage(
                content="Not a message. ping auburn if you see this.",
                flags=EPHEMERAL
            )
        )
        return response

    guild_id = body.guild_id

    async with engine.begin() as conn:
        try:
            cred = await get_disc_guild_credential(guild_id, conn)
            publisher = await get_publisher_by_discord_guild_credential(cred, conn)
        except DiscordGuildCredentialNotFoundException:
            response = MessageInteractionResponse(
                data=InteractionMessage(
                    content="This server is not registered. Use /register first.",
                    flags=EPHEMERAL
                )
            )
            return response

    data = body.data
    logger.info(data)
    if not data.resolved:
        response = MessageInteractionResponse(
            data=InteractionMessage(
                content="Resolved not present. This is a bug, ping auburn.",
                flags=EPHEMERAL
            )
        )
        return response

    all_attachments: List[DiscordAttachment] = []

    for _, value in data.resolved.messages.items():
        for attachment in value.attachments:
            all_attachments.append(attachment)

    if not all_attachments:
        response = MessageInteractionResponse(
            data=InteractionMessage(
                content="The message does not have attachments",
                flags=EPHEMERAL
            )
        )
        return response

    final_content = f"Found {len(all_attachments)} level(s) in the message:\n\n"
    
    for attachment in all_attachments:
        scopes = OrchardAuthScopes(
            Publisher_add=PublisherAddScope(
                publisher_id=publisher.id,
                url=attachment.url
            )
        )
        token = make_token_now(scopes, timedelta(hours=2))
        link = make_publisher_link("add", publisher_token=token)
        final_content = final_content + f"* `{attachment.filename}`: [click here]({link})\n"

    response = MessageInteractionResponse(
        data=InteractionMessage(
            content=final_content,
            flags=EPHEMERAL
        )
    )
    return response

HANDLERS = {
    "register": discord_register_handler,
    "version": version_handler,
    "add": add_handler
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
    return link

def make_publisher_link_continue(
    command_name: str,
    guild_token: Optional[str] = None,
    publisher_token: Optional[str] = None,
) -> str:
    link = make_publisher_link(command_name, guild_token, publisher_token)
    return f"Click [here]({link}) to continue"


@msgspec_return(200)
async def interaction_handler(request: Request):
    # check the discord headers.
    headers = request.headers
    try:
        sig = headers["X-Signature-Ed25519"]
        timestamp = headers["X-Signature-Timestamp"]
    except KeyError:
        raise MissingDiscordSignatureHeaders()

    public_key = config().DISCORD_PUBLIC_KEY
    verify_key = Ed25519PublicKey.from_public_bytes(bytes.fromhex(public_key))
    payload = await request.body()
    # concat bytes together
    to_verify = timestamp.encode("ascii") + payload

    try:
        verify_key.verify(bytes.fromhex(sig), to_verify)
    except InvalidSignature:
        raise InvalidDiscordSignature()

    # we're past the discord auth!
    body = msgspec.json.decode(payload, type=AnyInteraction)
    # first handle PING as usual.
    if isinstance(body, PingInteraction):
        return PongInteractionResponse()

    if isinstance(body, ApplicationCommandInteraction):
        try:
            return await HANDLERS[body.data.name](body)
        except KeyError:
            content = dedent(f"I don't know what to do with the command {body.data.name}. This is a bug, please ping auburn!")
            response = MessageInteractionResponse(
                data=InteractionMessage(
                    content=content,
                    flags=EPHEMERAL
                )
            )
            return response