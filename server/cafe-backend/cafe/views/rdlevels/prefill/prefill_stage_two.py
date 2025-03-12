from rules.contrib.views import objectgetter, permission_required
from cafe.views.types import AuthenticatedHttpRequest
from cafe.models.rdlevels.prefill import RDLevelPrefillResult
from django.shortcuts import get_object_or_404

from django_bridge.response import Response

@permission_required('cafe.can_make_levels_from_rdlevelprefillresult', fn=objectgetter(RDLevelPrefillResult, 'prefill_id'))
def prefill_stage_two(request: AuthenticatedHttpRequest, prefill_id: str):
    prefill = get_object_or_404(RDLevelPrefillResult, pk=prefill_id)
    render_data = {
        "prefill": prefill.to_dict()
    }
    return Response(request, request.resolver_match.view_name, render_data)