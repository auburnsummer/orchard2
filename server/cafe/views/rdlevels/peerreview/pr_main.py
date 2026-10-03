from django.http import JsonResponse
from cafe.views.types import HttpRequest
from cafe.models.rdlevels.rdlevel import RDLevel
from rules.contrib.views import objectgetter, permission_required

from cafe.bridge.response import Response

@permission_required('cafe.peerreview_rdlevel')
def pr_main(request: HttpRequest) -> JsonResponse:
    """
    View to display levels pending peer review.
    """
    # we want the oldest level first
    pr_levels = RDLevel.objects.filter(approval=0).order_by('last_updated')
    props = {
        "levels": [level.to_dict() for level in pr_levels]
    }

    return Response(request, request.resolver_match.view_name, props)