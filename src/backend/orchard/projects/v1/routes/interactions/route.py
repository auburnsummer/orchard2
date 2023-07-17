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

from re import A
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from orchard.projects.v1.core.config import config
from orchard import __version__
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.exceptions import InvalidSignature
from textwrap import dedent

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



async def interaction_handler(request: Request):
    # check the discord headers.
    headers = request.headers
    try:
        sig = headers["X-Signature-Ed25519"]
        timestamp = headers["X-Signature-Timestamp"]
    except KeyError:
        return JSONResponse(status_code=401, content={"error": "Missing req'd Discord headers"})

    public_key = config().DISCORD_PUBLIC_KEY
    verify_key = Ed25519PublicKey.from_public_bytes(bytes.fromhex(public_key))
    payload = await request.body()
    # concat bytes together
    to_verify = timestamp.encode("ascii") + payload

    try:
        verify_key.verify(bytes.fromhex(sig), to_verify)
    except InvalidSignature:
        return JSONResponse(status_code=401, content={"error": "Invalid request signature"})

    # we're past the discord auth!
    body = msgspec.json.decode(payload, type=BaseInteraction)
    # first handle PING as usual.
    if body.type == InteractionType.PING:
        payload = msgspec.json.encode(PongInteractionResponse())
        return Response(status_code=200, content=payload, headers={"content-type": "application/json"})
    
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
            payload = msgspec.json.encode(response)
            return Response(status_code=200, content=payload, headers={"content-type": "application/json"})
        else:
            pass



