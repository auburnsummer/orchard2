# nb: discord has more than this, but I'm only filling out as much in these structs as i'm using. 
from __future__ import annotations

from typing import Any, List, Literal, Never, Optional, Union
import msgspec

from enum import IntEnum

# Interactions.
class InteractionType(IntEnum):
    PING = 1
    APPLICATION_COMMAND = 2

class BaseInteraction(msgspec.Struct, kw_only=True, tag_field="type"):
    id: str


class PingInteraction(BaseInteraction, tag=InteractionType.PING.value):
    pass

class ApplicationCommandInteraction(BaseInteraction, tag=InteractionType.APPLICATION_COMMAND.value):
    guild_id: str  # we don't support DMs. So this will always be a value.
    data: Union[ChatInputApplicationCommandData, MessageApplicationCommandData]

AnyInteraction = Union[PingInteraction, ApplicationCommandInteraction]

class ApplicationCommandType(IntEnum):
    CHAT_INPUT = 1
    # USER = 2  (not used)
    MESSAGE = 3

class BaseApplicationCommandData(msgspec.Struct, kw_only=True, tag_field="type"):
    id: str
    name: str

class ChatInputApplicationCommandData(BaseApplicationCommandData, tag=ApplicationCommandType.CHAT_INPUT.value):
    pass

class MessageApplicationCommandData(BaseApplicationCommandData, tag=ApplicationCommandType.MESSAGE.value):
    target_id: str
    resolved: Optional[Resolved] = None

class DiscordMessage(msgspec.Struct):
    id: str
    channel_id: str
    attachments: List[DiscordAttachment]

class DiscordAttachment(msgspec.Struct, kw_only=True):
    id: str
    filename: str
    content_type: Optional[str] = None
    size: int
    url: str
    proxy_url: str

class Resolved(msgspec.Struct):
    messages: Optional[dict[str, DiscordMessage]] = None


class InteractionCallbackType(IntEnum):
    PONG = 1
    CHANNEL_MESSAGE_WITH_SOURCE = 4

class InteractionResponse(msgspec.Struct, kw_only=True, tag_field="type"):
    data: Optional[Any]

class PongInteractionResponse(InteractionResponse, tag=InteractionCallbackType.PONG.value):
    data: None = None

NOT_EPHEMERAL = 0
EPHEMERAL = 1 << 6

class InteractionMessage(msgspec.Struct):
    content: str
    flags: int

class MessageInteractionResponse(InteractionResponse, tag=InteractionCallbackType.CHANNEL_MESSAGE_WITH_SOURCE.value):
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