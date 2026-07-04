from django.http import JsonResponse
from cafe.views.types import HttpRequest
from rules.contrib.views import permission_required

from cafe.bridge.response import Response

@permission_required('cafe.peerreview_rdlevel')
def pharmacy_main(request: HttpRequest) -> JsonResponse:
    """
    Main menu for pharmacy section (admin controls)
    """

    return Response(request, request.resolver_match.view_name, {})