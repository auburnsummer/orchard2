from django.shortcuts import render, get_object_or_404
from rules.contrib.views import permission_required, objectgetter

from cafe.models import Club, ClubMembership
from cafe.views.types import AuthenticatedHttpRequest

from django_bridge.response import Response

@permission_required('cafe.view_member_of_club', fn=objectgetter(Club, 'club_id'))
def members(request: AuthenticatedHttpRequest, club_id: str):
    club = get_object_or_404(Club, pk=club_id)
    roles = ["owner", "admin"]

    def sort(membership: ClubMembership):
        return roles.index(membership.role)

    memberships = sorted(club.memberships.all(), key=sort)

    user_role = None
    for membership in memberships:
        if membership.user == request.user:
            user_role = membership.role
            break

    render_data = {
        "memberships": [ m.to_dict() for m in memberships ],
        "club": club.to_dict(),
        "user_role": user_role
    }
    return Response(request, request.resolver_match.view_name, render_data)
