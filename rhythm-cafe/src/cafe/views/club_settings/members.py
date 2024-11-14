from django.shortcuts import render, get_object_or_404
from rules.contrib.views import permission_required, objectgetter

from cafe.models import Club, ClubMembership

@permission_required('cafe.view_member_of_club', fn=objectgetter(Club, 'club_id'))
def members(request, club_id):
    club = get_object_or_404(Club, pk=club_id)
    roles = ["owner", "admin"]

    def sort(membership):
        return roles.index(membership.role)

    memberships = sorted(club.memberships.all(), key=sort)

    user_role = None
    for membership in memberships:
        if membership.user == request.user:
            user_role = membership.role
            break

    render_data = {
        "memberships": memberships,
        "current_club": club,
        "user_role": user_role
    }
    return render(request, "cafe/club_settings/members.jinja", render_data)
