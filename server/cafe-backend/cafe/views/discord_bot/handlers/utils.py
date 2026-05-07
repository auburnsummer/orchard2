from enum import Enum
from sre_parse import FLAGS

from django.http import JsonResponse
from cafe.models.discord_guild import DiscordGuild

class InteractionType(Enum):
    PING = 1
    APPLICATION_COMMAND = 2
    MESSAGE_COMPONENT = 3
    APPLICATION_COMMAND_AUTOCOMPLETE = 4
    MODAL_SUBMIT = 5

# https://docs.discord.com/developers/interactions/receiving-and-responding#interaction-response-object
# just contains what we use!
class ResponseType(Enum):
    PONG = 1
    CHANNEL_MESSAGE_WITH_SOURCE = 4
    DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE = 5
    UPDATE_ORIGINAL_MESSAGE = 7
    MODAL = 9

class Flags(Enum):
    EPHEMERAL = 1 << 6
    IS_COMPONENTS_V2 = 1 << 15

class ComponentType(Enum):
    TEXT_DISPLAY = 10
    STRING_SELECT = 3
    ACTION_ROW = 1
    BUTTON = 2
    CHECKBOX = 23
    LABEL = 18
    SEPERATOR = 14
    TEXT_INPUT = 4

def text(content):
    return {
        "type": ComponentType.TEXT_DISPLAY.value,
        "content": content
    }

def seperator():
    return {
        "type": ComponentType.SEPERATOR.value
    }

def action_row(*components):
    return {
        "type": ComponentType.ACTION_ROW.value,
        "components": list(components)
    }

def string_select(custom_id, options, placeholder=None):
    result = {
        "type": ComponentType.STRING_SELECT.value,
        "custom_id": custom_id,
        "options": options
    }
    if placeholder is not None:
        result["placeholder"] = placeholder
    return result

def option(label, value, default=False):
    return {
        "label": label,
        "value": value,
        "default": default
    }

def button(custom_id, label, style):
    return {
        "type": ComponentType.BUTTON.value,
        "custom_id": custom_id,
        "label": label,
        "style": style
    }

def label(label_text, component, description=None):
    result = {
        "type": ComponentType.LABEL.value,
        "label": label_text,
        "component": component
    }
    if description is not None:
        result["description"] = description
    return result

def text_input(custom_id, style=1, placeholder=None, required=True):
    result = {
        "type": ComponentType.TEXT_INPUT.value,
        "custom_id": custom_id,
        "style": style
    }
    if placeholder is not None:
        result["placeholder"] = placeholder
    if not required:
        result["required"] = False
    return result

def checkbox(custom_id, default=False):
    result = {
        "type": ComponentType.CHECKBOX.value,
        "custom_id": custom_id,
    }
    if default:
        result["default"] = True
    return result

def ephemeral_response(content):
    return JsonResponse({
        "type": ResponseType.CHANNEL_MESSAGE_WITH_SOURCE.value,
        "data": {
            "content": content,
            "flags": Flags.EPHEMERAL.value
        },
    })

def deferred_response():
    return JsonResponse({
        "type": ResponseType.DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE.value,
        "data": {
            "flags": Flags.EPHEMERAL.value
        },
    })

def test_message_component_response():
    return JsonResponse({
        "type": ResponseType.CHANNEL_MESSAGE_WITH_SOURCE.value,
        "data": {
            "flags": Flags.EPHEMERAL.value,
            "components": [
                {
                    "type": ComponentType.TEXT_DISPLAY.value,
                    "content": "This is a message using the Text Display component"
                }
            ]
        },
    })

def get_club_from_guild_id(guild_id: str):
    try:
        dg = DiscordGuild.objects.get(id=guild_id)
    except DiscordGuild.DoesNotExist:
        return None
    
    if not dg.club:
        return None
    
    return dg.club