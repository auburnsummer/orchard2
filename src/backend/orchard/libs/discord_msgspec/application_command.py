from __future__ import annotations

from typing import Optional

from .interaction import ApplicationCommandType
from .base import BaseDiscordStruct

class ApplicationCommand(BaseDiscordStruct):
    """
    https://discord.com/developers/docs/interactions/application-commands#application-command-object
    """
    name: str
    description: Optional[str] = None
    type: ApplicationCommandType = ApplicationCommandType.CHAT_INPUT
    default_member_permissions: str = "0"
    dm_permission: bool = False