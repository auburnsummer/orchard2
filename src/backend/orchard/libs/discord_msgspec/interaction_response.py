from __future__ import annotations

from enum import IntEnum
from typing import Optional

from .base import BaseDiscordStruct

class InteractionCallbackType(IntEnum):
    """
    https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-response-object-interaction-callback-type
    """
    PONG = 1
    CHANNEL_MESSAGE_WITH_SOURCE = 4


class InteractionResponse(BaseDiscordStruct, tag_field="type"):
    """
    https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-response-object
    """

class PongInteractionResponse(InteractionResponse, tag=InteractionCallbackType.PONG.value):
    """
    https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-response-object-interaction-callback-type
    """

class MessageInteractionResponse(InteractionResponse, tag=InteractionCallbackType.CHANNEL_MESSAGE_WITH_SOURCE.value):
    data: MessageInteractionCallbackData

NOT_EPHEMERAL = 0
EPHEMERAL = 1 << 6

class MessageInteractionCallbackData(BaseDiscordStruct):
    """
    https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-response-object-messages
    """
    tts: Optional[bool] = False
    content: Optional[str] = None
    flags: Optional[int] = None
    # embeds
    # components