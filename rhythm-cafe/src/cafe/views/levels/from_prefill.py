from django.shortcuts import get_object_or_404, render
from cafe.models import RDLevelPrefillResult

from django.contrib.auth.decorators import login_required

import json

@login_required
def from_prefill(request, prefill_id):
    prefill = get_object_or_404(RDLevelPrefillResult, id=prefill_id)
    render_data = {
        "result": json.loads(prefill.data)
    }
    return render(request, "cafe/levels/from_prefill.jinja", {
        "prefill": render_data
    })