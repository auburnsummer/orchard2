from django.shortcuts import get_object_or_404
from django_bridge.response import Response

from cafe.models import RDLevel
from cafe.views.types import HttpRequest
from rules.contrib.views import objectgetter, permission_required

@permission_required('cafe.peerreview_rdlevel')
def pr_rdlevel(request: HttpRequest, level_id: str):
    rdlevel = get_object_or_404(RDLevel, id=level_id)
    # we want the oldest level first
    pr_levels = RDLevel.objects.filter(approval=0).order_by('last_updated')
    props = {
        "levels": [level.to_dict() for level in pr_levels],
        "rdlevel": rdlevel.to_dict(),
    }

    return Response(request, request.resolver_match.view_name, props)