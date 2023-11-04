from __future__ import annotations

from enum import IntEnum
from typing import Optional, Union

from .message import DiscordMessage
from .base import BaseDiscordStruct


# Interactions.
class InteractionType(IntEnum):
    """
    https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object-interaction-type
    """
    PING = 1
    APPLICATION_COMMAND = 2


class BaseInteraction(BaseDiscordStruct, tag_field="type"):
    """
    https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object-interaction-structure
    """
    id: str
    application_id: str
    token: str

class PingInteraction(BaseInteraction, tag=InteractionType.PING.value):
    """
    ping does not have data field
    https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object-interaction-data
    """


class ApplicationCommandType(IntEnum):
    """
    https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-types
    """
    CHAT_INPUT = 1
    # USER = 2  (not used)
    MESSAGE = 3

class BaseApplicationCommandData(BaseDiscordStruct, tag_field="type"):
    """
    https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object-interaction-data
    """
    id: str
    name: str

class ChatInputApplicationCommandData(BaseApplicationCommandData, tag=ApplicationCommandType.CHAT_INPUT.value):
    """
    https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object-interaction-data
    """

class MessageApplicationCommandData(BaseApplicationCommandData, tag=ApplicationCommandType.MESSAGE.value):
    """
    https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object-interaction-data
    """
    target_id: str
    resolved: Optional[Resolved] = None

class ApplicationCommandInteraction(BaseInteraction, tag=InteractionType.APPLICATION_COMMAND.value):
    """
    https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object-interaction-structure

    type=2
    """
    guild_id: str  # we don't support DMs. So this will always be a value.
    data: Union[ChatInputApplicationCommandData, MessageApplicationCommandData]

AnyInteraction = Union[PingInteraction, ApplicationCommandInteraction]

class Resolved(BaseDiscordStruct):
    """
    https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object-interaction-data
    """
    messages: Optional[dict[str, DiscordMessage]] = None
