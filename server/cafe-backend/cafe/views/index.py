from django.http import HttpResponse
from django_bridge.response import Response
import datetime

def index(request):
    now = datetime.datetime.now()
    return Response(request, "Home", {"time": now})