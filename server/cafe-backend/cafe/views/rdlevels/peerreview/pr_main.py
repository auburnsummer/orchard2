from django.http import JsonResponse
from cafe.views.types import HttpRequest
from cafe.models.rdlevels.rdlevel import RDLevel

from django_bridge.response import Response

def pr_main(request: HttpRequest) -> JsonResponse:
    """
    View to display levels pending peer review.
    """
    pr_levels = RDLevel.objects.filter(approval=0)
    props = {
        "levels": [level.to_dict() for level in pr_levels]
    }

    return Response(request, request.resolver_match.view_name, props)