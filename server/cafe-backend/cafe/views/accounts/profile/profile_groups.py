from allauth.account.decorators import login_required
from django_bridge.response import Response

from cafe.views.types import AuthenticatedHttpRequest

@login_required
def profile_groups(request: AuthenticatedHttpRequest):
    user = request.user
    render_data = [
        {
            "club": membership.club.to_dict(),
            "role": membership.role
        } for membership in user.memberships.all()
    ]
    return Response(request, "Profile", {"subpage": "groups", "clubs": render_data})