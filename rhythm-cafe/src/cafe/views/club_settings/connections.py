from django.shortcuts import get_object_or_404, render
from cafe.models import Club

from orchard.settings import DISCORD_BOT_INVITE_URL

# eh I don't have to be that great for the club UI
# since most people won't see it

# so for this one, we're just displaying the guild IDs directly
# instead of attempting to resolve them into the guild name (which takes an api call)

def connections(request, club_id):

    club = get_object_or_404(Club, pk=club_id)

    render_data = {
        "current_club": club,
        "DISCORD_BOT_INVITE_URL": DISCORD_BOT_INVITE_URL
    }

    return render(request, "cafe/club_settings/connections.jinja", render_data)