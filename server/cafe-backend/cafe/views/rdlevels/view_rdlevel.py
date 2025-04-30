from django.shortcuts import get_object_or_404
from django_bridge.response import Response

from cafe.models import RDLevel
from cafe.views.types import AuthenticatedHttpRequest


def view_rdlevel(request: AuthenticatedHttpRequest, level_id: str):
    rdlevel = get_object_or_404(RDLevel, id=level_id)
    props = {
        "rdlevel": rdlevel.to_dict()
    }
    return Response(request, request.resolver_match.view_name, props)