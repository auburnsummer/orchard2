from django_bridge.response import Response

def index(request):
    return Response(request, "Home", {})