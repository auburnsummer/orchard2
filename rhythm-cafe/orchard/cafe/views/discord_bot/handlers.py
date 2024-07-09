from textwrap import dedent
from django.http import HttpResponseRedirect, JsonResponse
from django.core.signing import TimestampSigner
from urllib.parse import urlencode

from django.urls import reverse

from orchard.settings import DOMAIN

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

    url = DOMAIN + reverse("cafe:connect_club_discord", args=[signed_token])
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


HANDLERS = {
    "version": version,
    "connectgroup": connectgroup
}