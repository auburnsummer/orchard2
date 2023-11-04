from typing import List, Optional

from .user import DiscordUser
from .base import BaseDiscordStruct
from .attachment import DiscordAttachment

class DiscordMessage(BaseDiscordStruct, kw_only=True):
    id: str
    channel_id: str
    attachments: List[DiscordAttachment]
    webhook_id: Optional[str] = None
    author: DiscordUser