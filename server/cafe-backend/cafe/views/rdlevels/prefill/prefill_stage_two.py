from django.contrib import messages
from rules.contrib.views import objectgetter, permission_required
from cafe.views.types import AuthenticatedHttpRequest
from cafe.models.rdlevels.prefill import RDLevelPrefillResult
from cafe.models.rdlevels.rdlevel import RDLevel
from cafe.views.rdlevels.common import AddLevelPayload
from django.shortcuts import get_object_or_404
from django import forms

from django_bridge.response import Response

import msgspec

class PrefillStageTwoPayload(forms.Form):
    prefill = forms.CharField()

@permission_required('cafe.can_make_levels_from_rdlevelprefillresult', fn=objectgetter(RDLevelPrefillResult, 'prefill_id'))
def prefill_stage_two(request: AuthenticatedHttpRequest, prefill_id: str):
    prefill = get_object_or_404(RDLevelPrefillResult, pk=prefill_id)
    if request.method == 'POST':
        form = PrefillStageTwoPayload(request.POST)
        if form.is_valid():
            prefill_data: str = form.cleaned_data.get("prefill")
            try:
                parsed = msgspec.json.decode(prefill_data, type=AddLevelPayload)
                args = {
                    **prefill.data,
                    **msgspec.structs.asdict(parsed),
                    "submitter": prefill.user,
                    "club": prefill.club
                }
                if args['icon_url'] is None:
                    args['icon_url'] = ''
                level = RDLevel(**args)
                level.save()
                messages.success(request, f"wow you clicked it! ${level.id}")
            except msgspec.ValidationError:
                messages.error(request, "An error occurred validating the level")
        else:
            messages.error(request, "An error occurred validating the form")

    render_data = {
        "prefill": prefill.to_dict()
    }
    return Response(request, request.resolver_match.view_name, render_data)