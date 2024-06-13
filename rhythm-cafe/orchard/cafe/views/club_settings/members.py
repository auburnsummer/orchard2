from django.shortcuts import render, get_object_or_404
from rules.contrib.views import permission_required, objectgetter

from cafe.models import Club, ClubMembership

@permission_required('cafe.view_member_of_club', fn=objectgetter(Club, 'club_id'))
def members(request, club_id):
    club = get_object_or_404(Club, pk=club_id)
    roles = ["owner", "admin"]

    memberships = { role: [membership.user for membership in club.clubmembership_set.filter(role__exact=role)] for role in roles}

    render_data = {
        "memberships": memberships
    }
    return render(request, "cafe/club_settings/members.jinja", render_data)
