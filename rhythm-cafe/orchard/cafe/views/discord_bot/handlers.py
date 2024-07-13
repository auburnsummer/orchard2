from textwrap import dedent
from django.http import HttpResponseRedirect, JsonResponse
from django.core.signing import TimestampSigner
from urllib.parse import urlencode

from django.urls import reverse

from orchard.settings import DOMAIN_URL

from cafe.models import DiscordGuild

connectgroup_signer = TimestampSigner(salt="connectgroup")

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
    guild_id = data['guild']['id']
    try:
        dg = DiscordGuild.objects.get(id=guild_id)
    except DiscordGuild.DoesNotExist:
        return not_found_response
    
    if not dg.club:
        return not_found_response
    
    return JsonResponse({
        "type": 4,
        "data": {
            "content": dedent(f"""
                {dg.club.name} (id: {dg.club.id})
            """),
            "flags": 1 << 6
        }
    })


HANDLERS = {
    "version": version,
    "connectgroup": connectgroup,
    "viewgroup": viewgroup
}