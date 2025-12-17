from django.http import HttpRequest, HttpResponse
from django_bridge.response import Response

from cafe.models.rdlevels import daily_blend

def index(request: HttpRequest) -> HttpResponse:
    daily_blend_level = daily_blend.get_todays_blend()
    props = {
        "daily_blend_level": daily_blend_level.to_dict() if daily_blend_level else None
    }
    return Response(request, request.resolver_match.view_name, props)