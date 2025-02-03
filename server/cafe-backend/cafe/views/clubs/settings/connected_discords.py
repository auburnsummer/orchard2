from django.shortcuts import get_object_or_404
from rules.contrib.views import permission_required, objectgetter

from cafe.models import Club
from cafe.models.discord_guild import DiscordGuild
from cafe.views.types import AuthenticatedHttpRequest

from django_bridge.response import Response

@permission_required('cafe.view_member_of_club', fn=objectgetter(Club, 'club_id'))
def connected_discords(request: AuthenticatedHttpRequest, club_id: str):
    club = get_object_or_404(Club, pk=club_id)

    guild_id = request.GET.get('guild_id')
    discord_guild = None
    did_check = False
    if guild_id:
        discord_guild = DiscordGuild.objects.filter(club=club, id=guild_id).first()
        did_check = True

    render_data = {
        "club": club.to_dict(),
        "discord_guild": discord_guild.to_dict() if discord_guild else None,
        "did_check": did_check
    }

    return Response(request, request.resolver_match.view_name, render_data)
