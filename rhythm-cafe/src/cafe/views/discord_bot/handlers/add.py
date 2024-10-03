from django.core.signing import TimestampSigner
from .utils import ephemeral_response, get_club_from_guild_id

from orchard.settings import DOMAIN_URL
from django.urls import reverse

addlevel_signer = TimestampSigner(salt="addlevel")

def _add(data, check_user_is_poster):
    not_found_response = ephemeral_response("No group found for this server (the server owner needs to use the `/connectgroup` command)")

    club = get_club_from_guild_id(data['guild']['id'])
    
    if not club:
        return not_found_response
        
    target_id = data['data']['target_id']
    attachments = [a for a in data['data']['resolved']['messages'][target_id]['attachments'] if a['filename'].endswith('.rdzip')]
    if not attachments:
        return ephemeral_response("The post doesn't have any attachments ending with .rdzip!")
    
    poster_id = data['data']['resolved']['messages'][target_id]['author']['id']
    invoker_id = data['member']['user']['id']

    if check_user_is_poster:
        if invoker_id != poster_id:
            return ephemeral_response("You can only add levels from posts you've made.")

    lines = []
    for attachment in attachments:
        payload = {
            "level_url": attachment['url'],
            # nb: this is the discord user id of the user who posted the message,
            # which may not be the same as the user who is running this command.
            "discord_user_id": poster_id,
            "club_id": club.id
        }
        print(payload)
        secret = addlevel_signer.sign_object(payload)
        url = DOMAIN_URL + reverse("cafe:level_add_s1", args=[secret])
        line = f"`{attachment['filename']}`: [click here]({url})"
        lines.append(line)

    content = "\n".join(f"- {line}" for line in lines)
    
    return ephemeral_response(content)

def add(data):
    return _add(data, check_user_is_poster=True)

def add_delegated(data):
    return _add(data, check_user_is_poster=False)