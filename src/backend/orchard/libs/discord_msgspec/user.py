from typing import Optional
from .base import BaseDiscordStruct

class DiscordUser(BaseDiscordStruct):
    """
    A discord user. There are more fields than this but this is probably all we'll ever be
    interested in.
    https://discord.com/developers/docs/resources/user#user-object-user-structure
    """
    id: str
    username: str
    global_name: Optional[str]
    avatar: Optional[str] = None
