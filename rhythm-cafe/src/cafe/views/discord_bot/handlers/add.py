from django.core.signing import TimestampSigner
from loguru import logger
from .utils import ephemeral_response, get_club_from_guild_id

from orchard.settings import DOMAIN_URL
from django.urls import reverse

addlevel_signer = TimestampSigner(salt="addlevel")

def add(data):
    not_found_response = ephemeral_response("No group found for this server (the server owner needs to use the `/connectgroup` command)")


    club = get_club_from_guild_id(data['guild']['id'])
    
    if not club:
        return not_found_response
    
    target_id = data['data']['target_id']
    attachments = [a for a in data['data']['resolved']['messages'][target_id]['attachments'] if a['filename'].endswith('.rdzip')]
    if not attachments:
        return ephemeral_response("The post doesn't have any attachments ending with .rdzip!")

    lines = []
    for attachment in attachments:
        secret = addlevel_signer.sign_object({
            "level_url": attachment['url'],
            "discord_user_id": data['member']['user']['id'],
            "club_id": club.id
        })
        url = DOMAIN_URL + reverse("cafe:level_add_s1", args=[secret])
        line = f"`{attachment['filename']}`: [click here]({url})"
        lines.append(line)

    content = "\n".join(f"- {line}" for line in lines)
    
    return ephemeral_response(content)