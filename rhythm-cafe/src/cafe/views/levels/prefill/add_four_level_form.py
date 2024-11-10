from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, render
from cafe.models import RDLevelPrefillResult, RDLevel
from django.urls import reverse

from django.contrib.auth.decorators import login_required

from rules.contrib.views import permission_required, objectgetter


import msgspec
import json

from cafe.views.levels.level.common import AddLevelPayload


def add_level_post(request, prefill: RDLevelPrefillResult):
    try:
        body = msgspec.json.decode(request.body, type=AddLevelPayload)
        args = {
            **prefill.data,
            **msgspec.structs.asdict(body),
            "submitter": prefill.user,
            "club": prefill.club
        }
        
        new_level = RDLevel(**args)
        new_level.save()

        payload = {
            "id": new_level.id,
            "url": reverse("cafe:level_view", args=[new_level.id])
        }

        return JsonResponse(payload)
    except msgspec.ValidationError as e:
        # return 401 error response
        return HttpResponseBadRequest(str(e))

def add_level_get(request, prefill: RDLevelPrefillResult):
    render_data = {
        "prefill": json.dumps(prefill.data),
        "club": prefill.club,
        "mode": 'new'
    }
    return render(request, "cafe/levels/edit_level.jinja", render_data)

@permission_required('prefill.can_access_prefill', fn=objectgetter(RDLevelPrefillResult, 'prefill_id'))
@login_required
def add_four_level_form(request, prefill_id):
    "Stage 4: This is the form that the user fills out, and then submits."
    prefill = get_object_or_404(RDLevelPrefillResult, id=prefill_id)
    if request.method == 'POST':
        return add_level_post(request, prefill)
    else:
        return add_level_get(request, prefill)