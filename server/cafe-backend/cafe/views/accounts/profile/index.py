from allauth.account.decorators import login_required
from cafe.bridge.response import Response
from cafe.views.types import AuthenticatedHttpRequest

@login_required
def profile(request: AuthenticatedHttpRequest):
    return Response(request, request.resolver_match.view_name, {})