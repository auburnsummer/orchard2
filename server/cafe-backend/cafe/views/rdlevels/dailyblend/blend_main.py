from django.http import JsonResponse
from cafe.views.types import HttpRequest
from rules.contrib.views import permission_required

from django_bridge.response import Response

@permission_required('cafe.blend_rdlevel')
def blend_main(request: HttpRequest) -> JsonResponse:
    return Response(request, request.resolver_match.view_name, {})