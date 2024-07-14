from django.http import JsonResponse
from cafe.models import DiscordGuild

def ephemeral_response(content):
    return JsonResponse({
        "type": 4,
        "data": {
            "content": content,
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