from typing import Optional
from .base import BaseDiscordStruct

class DiscordAttachment(BaseDiscordStruct, kw_only=True):
    "https://discord.com/developers/docs/resources/channel#attachment-object-attachment-structure"
    id: str
    filename: str
    content_type: Optional[str] = None
    size: int
    url: str
    proxy_url: str