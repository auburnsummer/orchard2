from allauth.account.decorators import login_required
from django_bridge.response import Response

@login_required
def profile(request):
    return Response(request, "Profile", {"subpage": "profile"})