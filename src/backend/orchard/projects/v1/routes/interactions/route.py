"""
Discord interactions.

Generally speaking, because I have the rhythm.cafe website, I _don't_ want to have to implement
UI twice. Once in a website, and once in Discord. So, the only thing Discord interactions do
is send a link to rhythm.cafe, which does the actual work.
"""

from datetime import timedelta
from orchard.libs.discord_msgspec.interaction import AnyInteraction, ApplicationCommandInteraction, MessageApplicationCommandData, PingInteraction
from orchard.libs.discord_msgspec.interaction_response import EPHEMERAL, MessageInteractionCallbackData, MessageInteractionResponse, PongInteractionResponse
from orchard.libs.utils.gen_id import IDType, gen_id
from orchard.projects.v1.core.auth import OrchardAuthScopes, PublisherRDPrefillScope, make_token_now
from orchard.projects.v1.core.exceptions import InvalidDiscordSignature, MissingDiscordSignatureHeaders
from orchard.projects.v1.core.wrapper import msgspec_return
from orchard.projects.v1.models.credentials import DiscordCredential
from orchard.projects.v1.models.discord_guild_credentials import DiscordGuildPublisherCredential
from orchard.projects.v1.models.engine import select
from starlette.requests import Request
from orchard.projects.v1.core.config import config
from orchard import __version__
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.exceptions import InvalidSignature
from textwrap import dedent

from typing import Optional

import msgspec

async def version_handler(_: ApplicationCommandInteraction):
    content = dedent(f"""
        ## Bot Version

        `{__version__}`
    """)
    response = MessageInteractionResponse(
        data=MessageInteractionCallbackData(
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
        data=MessageInteractionCallbackData(
            content=content,
            flags=EPHEMERAL
        )
    )
    return response


async def add_handler(body: ApplicationCommandInteraction):
    def error(message: str):
        response = MessageInteractionResponse(
            data=MessageInteractionCallbackData(
                content=message,
                flags=EPHEMERAL
            )
        )
        return response
    
    # add should always be on a message.
    if not isinstance(body.data, MessageApplicationCommandData):
        return error("/add used on something that's not a message, ping auburn if you see this.")

    guild_id = body.guild_id

    cred = select(DiscordGuildPublisherCredential).by_id(guild_id)

    if not cred:
        return error("This server is not registered. Use /register first.")

    publisher = cred.publisher

    data = body.data
    if not data.resolved or not data.resolved.messages:
        return error("Discord did not give us resolved data. This is a bug, ping auburn if you see this")

    try:
        message = data.resolved.messages[data.target_id]
    except KeyError:
        return error("target_id not given in resolved data. This is a bug, ping auburn if you see this")

    if len(message.attachments) == 0:
        return error("No attachments in this message")

    final_content = f"Found {len(message.attachments)} level(s) in the message:\n\n"

    cred = DiscordCredential.get_or_create(message.author.id, message.author.global_name)
    user = cred.user
    
    for attachment in message.attachments:
        # create a scoped token to use the /prefill and /identify endpoints
        # the token to use the /add endpoint is returned from the /prefill endpoint.
        scopes = OrchardAuthScopes(
            Publisher_rdprefill=PublisherRDPrefillScope(
                publisher_id=publisher.id,
                user_id=user.id,
                url=attachment.url,
                link_id=gen_id(IDType.PREFILL)
            ),
            Publisher_identify=publisher.id
        )
        token = make_token_now(scopes, timedelta(hours=2))
        link = make_publisher_link("add/rd", publisher_token=token)
        final_content = final_content + f"* `{attachment.filename}`: [click here]({link})\n"

    response = MessageInteractionResponse(
        data=MessageInteractionCallbackData(
            content=final_content,
            flags=EPHEMERAL
        )
    )
    return response

HANDLERS = {
    "register": discord_register_handler,
    "version": version_handler,
    "Add to Rhythm Cafe": add_handler,
    "Add to Rhythm Cafe (delegated)": add_handler
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
    except InvalidSignature as exc:
        raise InvalidDiscordSignature() from exc

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
                data=MessageInteractionCallbackData(
                    content=content,
                    flags=EPHEMERAL
                )
            )
            return response