from django.http import HttpRequest, HttpResponse
from django_bridge.response import Response

def index(request: HttpRequest) -> HttpResponse:
    return Response(request, "Home", {})