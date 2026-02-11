from django import forms
from django.http import JsonResponse
from loguru import logger
from cafe.models.rdlevels.rdlevel import select_rdlevel_by_id_or_url
from cafe.views.types import HttpRequest
from rules.contrib.views import permission_required

from cafe.models.rdlevels.blend_random_pool import DailyBlendRandomPool

from django_bridge.response import Response

from django.contrib import messages

class BlendPoolForm(forms.Form):
    level_id = forms.CharField()
    action = forms.CharField()

@permission_required('cafe.blend_rdlevel')
def blend_pool(request: HttpRequest) -> JsonResponse:
    if request.method == "POST":
        form = BlendPoolForm(request.POST)
        if form.is_valid():
            level_id = form.cleaned_data["level_id"]
            action = form.cleaned_data["action"]

            logger.info(action)
            logger.info(level_id)

            level = select_rdlevel_by_id_or_url(level_id)

            if not level:
                messages.error(request, f"Level with ID {level_id} does not exist.")
                return Response(request, request.resolver_match.view_name, {})

            if action == "add":
                DailyBlendRandomPool.objects.get_or_create(level=level)
            elif action == "remove":
                DailyBlendRandomPool.objects.filter(level=level).delete()
        else:
            logger.warning("Invalid form data submitted to blend_pool")
            messages.error(request, "Invalid data submitted.")

    pool = DailyBlendRandomPool.objects.all()

    props = {
        "pool": [pool_item.to_dict() for pool_item in pool],
    }

    return Response(request, request.resolver_match.view_name, props)