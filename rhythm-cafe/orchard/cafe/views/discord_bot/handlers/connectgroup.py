from django.core.signing import TimestampSigner
from orchard.settings import DOMAIN_URL
from django.urls import reverse

from textwrap import dedent

from .utils import ephemeral_response

connectgroup_signer = TimestampSigner(salt="connectgroup")

def connectgroup(data):
    guild_id = data['guild']['id']
    signed_token = connectgroup_signer.sign(guild_id)

    url = DOMAIN_URL + reverse("cafe:connect_club_discord", args=[signed_token])
    content = dedent(f"""
        ## Connect

        Click [this link]({url}) to continue!
        
        _Note: do not share this link._
    """)
    return ephemeral_response(content)