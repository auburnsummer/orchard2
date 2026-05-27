from django import forms
from django.http import JsonResponse
from loguru import logger
from cafe.views.types import HttpRequest
from rules.contrib.views import permission_required

from cafe.models.rdlevels.blend_random_pool import DailyBlendRandomPool
from cafe.models.rdlevels.blend_pool import BlendPool
from cafe.models.rdlevels.rdlevel import RDLevel

from django.shortcuts import get_object_or_404

from cafe.bridge.response import Response

from django.contrib import messages

class BlendPoolForm(forms.Form):
    level_id = forms.CharField()
    action = forms.CharField()
    tickets = forms.IntegerField(required=False, min_value=1)

@permission_required('cafe.blend_rdlevel')
def blend_pool(request: HttpRequest, pool_id: str) -> JsonResponse:
    pool = get_object_or_404(BlendPool, id=pool_id)

    if request.method == "POST":
        form = BlendPoolForm(request.POST)
        if form.is_valid():
            level_id = form.cleaned_data["level_id"]
            action = form.cleaned_data["action"]

            level = RDLevel.objects.filter(id=level_id).first()

            if level:
                if action == "add":
                    DailyBlendRandomPool.objects.get_or_create(level=level, pool=pool)
                elif action == "remove":
                    DailyBlendRandomPool.objects.filter(level=level, pool=pool).delete()
                elif action == "ticket":
                    tickets = form.cleaned_data.get("tickets", 1)
                    if not form.cleaned_data.get("tickets"):
                        messages.error(request, "Ticket value missing")
                    else:
                        DailyBlendRandomPool.objects.filter(level=level, pool=pool).update(tickets=tickets)
            else:
                messages.error(request, f"Level with ID {level_id} does not exist.")
        else:
            logger.warning("Invalid form data submitted to blend_pool")
            messages.error(request, "Invalid data submitted.")

    pool_items = DailyBlendRandomPool.objects.filter(pool=pool)

    props = {
        "pool": pool.to_dict(),
        "pool_items": [pool_item.to_dict() for pool_item in pool_items],
    }

    return Response(request, request.resolver_match.view_name, props)