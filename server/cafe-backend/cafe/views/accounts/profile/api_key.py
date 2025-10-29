from allauth.account.decorators import login_required
from django_bridge.response import Response
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST

from cafe.views.types import AuthenticatedHttpRequest


@login_required
def api_key_view(request: AuthenticatedHttpRequest) -> HttpResponse:
    """
    Display the API key management page.
    
    Note: We can't show the actual API key since it's a signed token.
    The key is only shown once when first generated.
    """
    has_api_key = request.user.api_key_iter > 0
    return Response(request, request.resolver_match.view_name, {
        "hasApiKey": has_api_key,
    })


@login_required
@require_POST
def generate_api_key(request: AuthenticatedHttpRequest) -> HttpResponse:
    """
    Generate a new API key for the user.
    
    Returns a cryptographically signed token that can't be retrieved later.
    """
    api_key = request.user.generate_api_key()
    messages.add_message(request, messages.SUCCESS, "API key generated! Make sure to copy it now - you won't be able to see it again.")
    return Response(request, "cafe:profile_api_key", {
        "hasApiKey": True,
        "apiKey": api_key,  # Only time the signed token is shown
    })


@login_required
@require_POST
def revoke_api_key(request: AuthenticatedHttpRequest) -> HttpResponse:
    """Revoke the user's API key."""
    request.user.revoke_api_key()
    messages.add_message(request, messages.SUCCESS, "API key revoked!")
    return Response(request, "cafe:profile_api_key", {
        "hasApiKey": False,
    })
