from django_bridge.response import Response

def profile(request):
    return Response(request, "Profile", {})