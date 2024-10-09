from django.forms import model_to_dict
from django.http import JsonResponse
from django.urls import reverse
from cafe.models import RDLevelPrefillResult
from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404

@login_required
def add_three_get_prefill_status(request, prefill_id):
    "Stage 3: The client polls the server for the prefill status, and redirects to the level add page if ready."
    prefill = get_object_or_404(RDLevelPrefillResult, id=prefill_id)
    payload = {
        "id": prefill.id,
        "ready": prefill.ready,
        "errors": prefill.errors,
    }
    if prefill.ready:
        payload["redirect_url"] = reverse("cafe:level_add_s4", kwargs={"prefill_id": prefill_id})
    return JsonResponse(payload)