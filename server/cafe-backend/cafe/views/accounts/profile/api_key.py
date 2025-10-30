from allauth.account.decorators import login_required
from django_bridge.response import Response
from django.http import HttpResponse

from cafe.views.types import AuthenticatedHttpRequest


@login_required
def api_key_view(request: AuthenticatedHttpRequest) -> HttpResponse:
    """
    Display the API key management page.
    
    Note: We can't show the actual API key since it's a signed token.
    The key is only shown once when first generated.
    """
    api_key = None
    if request.method == "POST":
        api_key = request.user.generate_api_key()
        
    has_api_key = request.user.api_key_iter > 0
    return Response(request, request.resolver_match.view_name, {
        "has_api_key": has_api_key,
        "api_key": api_key
    })
