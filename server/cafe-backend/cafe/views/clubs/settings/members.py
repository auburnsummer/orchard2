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

    memberships_render_data = []
    for membership in memberships:
        permissions = {
            "can_change": request.user.has_perm("cafe.change_clubmembership", membership),
            "can_delete": request.user.has_perm("cafe.delete_clubmembership", membership)
        }
        memberships_render_data.append({
            "membership": membership.to_dict(),
            "permissions": permissions
        })

    render_data = {
        "memberships": memberships_render_data,
        "club": club.to_dict(),
        "can_add": request.user.has_perm("cafe.create_invite_for_club", club)
    }
    return Response(request, request.resolver_match.view_name, render_data)
