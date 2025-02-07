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
    message = data['data']['resolved']['messages'][target_id]
    attachments = [a for a in message['attachments'] if a['filename'].endswith('.rdzip')]
    if not attachments:
        return ephemeral_response("The post doesn't have any attachments ending with .rdzip!")
    
    is_webhook = 'webhook_id' in message
    invoker_id = data['member']['user']['id']
    # nb: poster_id is the discord user id of the user who will be credited as the submitter of the level.
    # poster_id is normally the user who posted the message,
    # but if the message was posted by a webhook, then the poster_id is the user who ran the command.
    # message['author']['id'] and invoker_id are not always the same,
    # such as in the delegated scenario where someone else is running the command on behalf of the poster.
    poster_id = message['author']['id'] if not is_webhook else invoker_id

    if check_user_is_poster:
        if is_webhook:
            return ephemeral_response("You can't add levels from webhooks.")
        if invoker_id != poster_id:
            return ephemeral_response("You can only add levels from your own messages.")

    lines = []
    for attachment in attachments:
        payload = {
            "level_url": attachment['url'],
            # nb: this is the discord user id of the user who posted the message,
            # which may not be the same as the user who is running this command.
            "discord_user_id": poster_id,
            # hint for name in case we need to create an account
            # nb: we don't need to check for the webhook scenario here, because
            # if it is a webhook scenario, then the poster_id is the user who ran the command,
            # who will always have an account by the time they reach the level submission portal.
            "discord_user_name_hint": message['author']['username'],
            "club_id": club.id
        }
        secret = addlevel_signer.sign_object(payload)
        url = DOMAIN_URL + reverse("cafe:level_portal", args=[secret])
        line = f"`{attachment['filename']}`: [click here]({url})"
        lines.append(line)

    content = "\n".join(f"- {line}" for line in lines)
    
    return ephemeral_response(content)

def add(data):
    return _add(data, check_user_is_poster=True)

def add_delegated(data):
    return _add(data, check_user_is_poster=False)