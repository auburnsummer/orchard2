from textwrap import dedent
from django.http import JsonResponse
from django.urls import reverse
from .utils import ephemeral_response, get_club_from_guild_id
from orchard.settings import DOMAIN_URL

def viewgroup(data):
    not_found_response = ephemeral_response("No group found for this server")
    club = get_club_from_guild_id(data['guild']['id'])
    if not club:
        return not_found_response
    
    club_settings_url = DOMAIN_URL + reverse('cafe:club_settings_info', args=[club.id])
    content = dedent(f"""
        {club.name} (id: {club.id})

        [Link to settings]({club_settings_url})     
    """)
    return ephemeral_response(content)