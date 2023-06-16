from sqlmodel import Field, Relationship, SQLModel, create_engine, JSON, Column
from pydantic import BaseModel
from typing import Any, Literal, Optional, List, Union
from enum import IntEnum, StrEnum

from datetime import datetime

class DiscordGuild(SQLModel, table=True):
    id: str = Field(primary_key=True)
    display_name: str


class DiscordMessage(SQLModel, table=True):
    message_id: str = Field(primary_key=True)
    channel_id: str
    guild_id: str = Field(foreign_key="discordguild.id")


# https://discord.com/developers/docs/reference#error-messages
class DiscordErrorResponse(BaseModel):
    code: int
    message: str
    errors: Any


class OAuthErrorResponse(BaseModel):
    error: str
    error_description: str


class OAuthTokenResponse(BaseModel):
    access_token: str
    expires_in: int
    refresh_token: str
    scope: str
    token_type: str


class DiscordUser(BaseModel):
    id: str
    """id of the discord user."""
    username: str
    """username of the discord user."""
    avatar: str
    """avatar hash of the user. to get the URL: https://cdn.discordapp.com/avatars/{id}/{avatar}.png"""


class DiscordChannelType(IntEnum):
    GUILD_TEXT = 0
    DM = 1
    GUILD_VOICE = 2
    GROUP_DM = 3
    GUILD_CATEGORY = 4
    GUILD_ANNOUNCEMENT = 5
    ANNOUNCEMENT_THREAD = 10
    PUBLIC_THREAD = 11
    PRIVATE_THREAD = 12
    GUILD_STAGE_VOICE = 13
    GUILD_DIRECTORY = 14
    GUILD_FORUM = 15


class DiscordChannelPartial(BaseModel):
    id: str
    type: DiscordChannelType
    name: Optional[str]
    permissions: Optional[str]


class DiscordInteractionType(IntEnum):
    PING = 1
    APPLICATION_COMMAND = 2
    MESSAGE_COMPONENT = 3
    APPLICATION_COMMAND_AUTOCOMPLETE = 4
    MODAL_SUBMIT = 5


class BaseInteraction(BaseModel):
    "All interaction payloads have these fields."
    id: str
    application_id: str
    type: DiscordInteractionType
    token: str
    version: int


class GuildMember(BaseModel):
    


class DataInteraction(BaseInteraction):
    "All interaction payloads with data have these fields. This is all interactions except PING."
    data: Any
    member: Optional[Any]


class ApplicationCommandType(IntEnum):
    CHAT_INPUT = 1
    USER = 2
    MESSAGE = 3


class ApplicationCommandOptionType(IntEnum):
    SUB_COMMAND = 1
    SUB_COMMAND_GROUP = 2
    STRING = 3
    INTEGER = 4
    BOOLEAN = 5
    USER = 6
    CHANNEL = 7
    ROLE = 8
    MENTIONABLE = 9
    NUMBER = 10
    ATTACHMENT = 11


class ApplicationCommandInteractionDataOption(BaseModel):
    name: str
    type: ApplicationCommandOptionType
    value: Optional[Union[str, int, float, bool]]


class ApplicationCommandPayload(BaseModel):
    id: str
    name: str  
    type: ApplicationCommandType
    resolved: Optional[Any]
    options: Optional[List[ApplicationCommandInteractionDataOption]]
    guild_id: Optional[str]
    target_id: Optional[str]



class SlashCommandInteraction(BaseModel):
    pass

# class DiscordInteraction(BaseModel):
#     id: str
#     application_id: str                                                                                                                                                                                            
#     type: DiscordInteractionType





class EmbedFooter(BaseModel):
    text: str
    icon_url: Optional[str]
    proxy_icon_url: Optional[str]


class EmbedImage(BaseModel):
    url: str
    proxy_url: Optional[str]
    height: Optional[int]
    width: Optional[int]


class EmbedProvider(BaseModel):
    name: Optional[str]
    url: Optional[str]


class EmbedAuthor(BaseModel):
    name: str
    url: Optional[str]
    icon_url: Optional[str]
    proxy_icon_url: Optional[str]


class EmbedThumbnail(BaseModel):
    url: str
    proxy_url: Optional[str]
    height: Optional[int]
    width: Optional[int]


class EmbedVideo(BaseModel):
    url: str
    proxy_url: Optional[str]
    height: Optional[int]
    width: Optional[int]


class EmbedField(BaseModel):
    name: str
    value: str
    inline: Optional[bool]


class Embed(BaseModel):
    title: Optional[str]
    description: Optional[str]
    url: Optional[str]
    timestamp: Optional[datetime]
    color: Optional[int]
    footer: Optional[EmbedFooter]
    image: Optional[EmbedImage]
    thumbnail: Optional[EmbedThumbnail]
    video: Optional[EmbedVideo]
    provider: Optional[EmbedProvider]
    author: Optional[EmbedAuthor]
    fields: Optional[List[EmbedField]]


class AllowedMentionParseType(StrEnum):
    ROLES = "roles"
    USERS = "users"
    EVERYONE = "everyone"


class AllowedMentions(BaseModel):
    parse: Optional[List[AllowedMentionParseType]]
    roles: Optional[List[str]]
    users: Optional[List[str]]
    replied_user: Optional[bool]


class InteractionCallbackPayload(BaseModel):
    tts: Optional[bool]
    content: Optional[str]
    embeds: Optional[List[Embed]]
    allowed_mentions: Optional[AllowedMentions]
    flags: Optional[int]
    components: Optional[Any]
    attachments: Optional[Any]


class ApplicationCommandOptionChoice(BaseModel):
    name: str
    value: Union[str, int, float]

class ApplicationCommandOption(BaseModel):
    type: ApplicationCommandOptionType
    name: str
    description: str
    required: Optional[bool]
    choices: Optional[List[ApplicationCommandOptionChoice]]
    channel_types: Optional[List[DiscordChannelType]]
    min_value: Optional[int | float]
    max_value: Optional[int | float]
    min_length: Optional[int]
    max_length: Optional[int]
    autocomplete: Optional[bool]


class ApplicationCommand(BaseModel):
    """
name	string	Name of command, 1-32 characters
name_localizations?	?dictionary with keys in available locales	Localization dictionary for the name field. Values follow the same restrictions as name
description?	string	1-100 character description for CHAT_INPUT commands
description_localizations?	?dictionary with keys in available locales	Localization dictionary for the description field. Values follow the same restrictions as description
options?	array of application command option	the parameters for the command
default_member_permissions?	?string	Set of permissions represented as a bit set
dm_permission?	?boolean	Indicates whether the command is available in DMs with the app, only for globally-scoped commands. By default, commands are visible.
default_permission?	boolean	Replaced by default_member_permissions and will be deprecated in the future. Indicates whether the command is enabled by default when the app is added to a guild. Defaults to true
type?	one of application command type	Type of command, defaults 1 if not set
nsfw?	boolean	Indicates whether the command is age-restricted
    """
    name: str
    description: Optional[str]
    options: Optional[List[ApplicationCommandOption]]
    default_member_permissions: Optional[str]
    dm_permission: Optional[bool]
    type: Optional[ApplicationCommandType]
    nsfw: Optional[bool]