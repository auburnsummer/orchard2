from textwrap import dedent
from django.http import HttpResponseRedirect, JsonResponse
from django.core.signing import TimestampSigner
from urllib.parse import urlencode

from django.urls import reverse

from orchard.settings import DOMAIN_URL

from cafe.models import DiscordGuild

connectgroup_signer = TimestampSigner(salt="connectgroup")
addlevel_signer = TimestampSigner(salt="addlevel")

def version(_data):
    return JsonResponse({
        "type": 4,
        "data": {
            "content": dedent(f"""
                ## Bot Version

                `0.0.1`
            """),
            "flags": 1 << 6
        },
    })

def connectgroup(data):
    guild_id = data['guild']['id']
    signed_token = connectgroup_signer.sign(guild_id)

    url = DOMAIN_URL + reverse("cafe:connect_club_discord", args=[signed_token])
    return JsonResponse({
        "type": 4,
        "data": {
            "content": dedent(f"""
                ## Connect

                Click [this link]({url}) to continue!
                
                _Note: do not share this link._
            """),
            "flags": 1 << 6
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


def viewgroup(data):
    not_found_response = JsonResponse({
        "type": 4,
        "data": {
            "content": dedent(f"""
                No group found for this server
            """),
            "flags": 1 << 6
        },
    })
    club = get_club_from_guild_id(data['guild']['id'])
    if not club:
        return not_found_response
    
    club_settings_url = DOMAIN_URL + reverse('cafe:club_settings_info', args=[club.id])
    return JsonResponse({
        "type": 4,
        "data": {
            "content": dedent(f"""
                {club.name} (id: {club.id})

                [Link to settings]({club_settings_url})
            """),
            "flags": 1 << 6
        }
    })

def add(data):
    not_found_response = JsonResponse({
        "type": 4,
        "data": {
            "content": dedent(f"""
                No group found for this server (the server owner needs to use the `/connectgroup` command)
            """),
            "flags": 1 << 6
        },
    })

    club = get_club_from_guild_id(data['guild']['id'])
    
    if not club:
        return not_found_response
    
    target_id = data['data']['target_id']
    attachments = [a for a in data['data']['resolved']['messages'][target_id]['attachments'] if a['filename'].endswith('.rdzip')]
    if not attachments:
        return JsonResponse({
            "type": 4,
            "data": {
                "content": dedent(f"""
                    The post doesn't have any attachments ending with .rdzip!
                """),
                "flags": 1 << 6
            },
        })

    lines = []
    for attachment in attachments:
        secret = addlevel_signer.sign_object({
            "level_url": attachment['proxy_url'],
            "club_id": club.id
        })
        url = DOMAIN_URL + reverse("cafe:level_add", args=[secret])
        line = f"`{attachment['filename']}`: [click here]({url})"
        lines.append(line)

    content = "\n".join(f"- {line}" for line in lines)
    
    return JsonResponse({
        "type": 4,
        "data": {
            "content": content,
            "flags": 1 << 6
        }
    })

HANDLERS = {
    "version": version,
    "connectgroup": connectgroup,
    "viewgroup": viewgroup,
    "Add level to Rhythm Café": add
}