from django.http import JsonResponse
from cafe.tasks.run_daily_blend import run_daily_blend_task
from cafe.views.types import HttpRequest
from rules.contrib.views import permission_required

from django.contrib import messages
from django_bridge.response import Response

@permission_required('cafe.blend_rdlevel')
def blend_now(request: HttpRequest) -> JsonResponse:
    if request.method == 'POST':
        run_daily_blend_task(True)
        messages.success(request, "Blend process started successfully.")

    return Response(request, request.resolver_match.view_name, {})