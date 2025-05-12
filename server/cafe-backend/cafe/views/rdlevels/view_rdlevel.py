from django.shortcuts import get_object_or_404
from django_bridge.response import Response

from cafe.models import RDLevel
from cafe.views.types import HttpRequest


def view_rdlevel(request: HttpRequest, level_id: str):
    rdlevel = get_object_or_404(RDLevel, id=level_id)
    props = {
        "rdlevel": rdlevel.to_dict(),
        "can_edit": request.user.has_perm("cafe.change_rdlevel", rdlevel),
        "can_delete": request.user.has_perm("cafe.delete_rdlevel", rdlevel),
    }
    return Response(request, request.resolver_match.view_name, props)