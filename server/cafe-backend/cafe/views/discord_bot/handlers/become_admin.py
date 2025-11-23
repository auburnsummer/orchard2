from .utils import ephemeral_response, get_club_from_guild_id
from cafe.models.rdlevels.tempuser import get_or_create_discord_user
from cafe.models.clubs.club_membership import ClubMembership
from orchard.settings import DOMAIN_URL
from django.urls import reverse

def becomeadmin(data):
    not_found_response = ephemeral_response("No group found for this server -- you probably should run `/connectgroup` first!")
    club = get_club_from_guild_id(data['guild']['id'])
    if not club:
        return not_found_response
    invoker_id = data['member']['user']['id']
    user = get_or_create_discord_user(invoker_id, data['member']['user'].get('global_name') or data['member']['user']['username'])
    membership = ClubMembership(
        user=user,
        club=club,
        role='admin'
    )
    try:
        membership.save()
    except Exception:
        return ephemeral_response("An error occurred while trying to make you an admin. maybe you already are one")

    club_settings_url = DOMAIN_URL + reverse('cafe:club_settings_info', args=[club.id])

    return ephemeral_response(f"You are now an admin of the group **{club.name}**! (id: {club.id})\n\n[Link to settings]({club_settings_url})")