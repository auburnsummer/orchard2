from django.shortcuts import render, get_object_or_404
from rules.contrib.views import permission_required, objectgetter

from cafe.models import Club

@permission_required('cafe.view_info_of_club', fn=objectgetter(Club, 'club_id'))
def info(request, club_id):
    club = get_object_or_404(Club, pk=club_id)

    render_data = {
        "current_club": club
    }
    return render(request, "cafe/club_settings/info.jinja", render_data)
