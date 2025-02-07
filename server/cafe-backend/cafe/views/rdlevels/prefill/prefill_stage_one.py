from rules.contrib.views import permission_required
from django_bridge.response import Response
from .predicates import register_imports

from cafe.views.types import AuthenticatedHttpRequest

register_imports()

@permission_required('prefill.ok', fn=lambda _, code: code)
def prefill_stage_one(request: AuthenticatedHttpRequest, code: str):
    render_data = {
        "code": code
    }
    
    return Response(request, request.resolver_match.view_name, render_data)
