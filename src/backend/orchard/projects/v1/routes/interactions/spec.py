# nb: discord has more than this, but I'm only filling out as much in these structs as i'm using. 
from __future__ import annotations

from typing import Any, Literal, Optional
import msgspec

from enum import IntEnum

class InteractionType(IntEnum):
    PING = 1
    APPLICATION_COMMAND = 2

class BaseInteraction(msgspec.Struct, kw_only=True):
    id: str
    type: InteractionType
    version: int
    guild_id: str  # we don't support DMs. So this will always be a value.
    target_id: Optional[str] = None

class ApplicationCommandInteractionPayload(msgspec.Struct):
    id: str
    name: str
    type: ApplicationCommandType

class ApplicationCommandResolvedData(msgspec.Struct):
    pass

class ApplicationCommandInteraction(BaseInteraction, kw_only=True):
    type: Literal[2] = 2
    data: ApplicationCommandInteractionPayload

class InteractionCallbackType(IntEnum):
    PONG = 1
    CHANNEL_MESSAGE_WITH_SOURCE = 4

class InteractionResponse(msgspec.Struct):
    type: InteractionCallbackType
    data: Optional[Any]

class PongInteractionResponse(InteractionResponse):
    type: Literal[1] = 1
    data: None = None

NOT_EPHEMERAL = 0
EPHEMERAL = 1 << 6

class InteractionMessage(msgspec.Struct):
    content: str
    flags: int

class MessageInteractionResponse(InteractionResponse, kw_only=True):
    # msgspec does not yet support enums in literals
    type: Literal[4] = 4
    data: InteractionMessage

class ApplicationCommandType(IntEnum):
    CHAT_INPUT = 1
    USER = 2
    MESSAGE = 3

class ApplicationCommand(msgspec.Struct):
    name: str
    description: Optional[str] = None
    type: ApplicationCommandType = ApplicationCommandType.CHAT_INPUT
    default_member_permissions: str = "0"
    dm_permission: bool = False