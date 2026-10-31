from cafe.bridge.response import Response
from cafe.views.rdlevels.peerreview.pr_levels import get_pr_pending_levels
from cafe.views.types import HttpRequest
from django.http import JsonResponse
from rules.contrib.views import permission_required


@permission_required('cafe.peerreview_rdlevel')
def pr_main(request: HttpRequest) -> JsonResponse:
    """
    View to display levels pending peer review.
    """
    pr_levels = get_pr_pending_levels()
    props = {
        "levels": [level.to_dict() for level in pr_levels]
    }

    return Response(request, request.resolver_match.view_name, props)