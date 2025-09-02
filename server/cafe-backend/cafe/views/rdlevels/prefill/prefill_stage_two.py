from django.contrib import messages
from django.db import transaction
from rules.contrib.views import objectgetter, permission_required
from cafe.views.types import AuthenticatedHttpRequest
from cafe.models.rdlevels.prefill import RDLevelPrefillResult
from cafe.models.rdlevels.rdlevel import RDLevel
from cafe.views.rdlevels.common import AddLevelPayload
from django.shortcuts import get_object_or_404, redirect
from django import forms

from django_bridge.response import Response

import msgspec

class PrefillStageTwoPayload(forms.Form):
    prefill = forms.CharField()

@permission_required('cafe.can_make_levels_from_rdlevelprefillresult', fn=objectgetter(RDLevelPrefillResult, 'prefill_id'))
def prefill_stage_two(request: AuthenticatedHttpRequest, prefill_id: str):
    prefill = get_object_or_404(RDLevelPrefillResult, pk=prefill_id)
    if request.method == 'POST':
        if prefill.prefill_type == 'new':
            # we're adding a level. JSON encoded data is provided by the client in the "prefill" form property.
            form = PrefillStageTwoPayload(request.POST)
            if form.is_valid():
                prefill_data: str = form.cleaned_data.get("prefill")
                try:
                    parsed = msgspec.json.decode(prefill_data, type=AddLevelPayload)
                    args = {
                        **prefill.data,
                        **msgspec.structs.asdict(parsed),
                        "approval": 0,
                        "submitter": prefill.user,
                        "club": prefill.club
                    }
                    if args['icon_url'] is None:
                        args['icon_url'] = ''
                    level = RDLevel(**args)
                    with transaction.atomic():
                        level.save()
                        prefill.delete()

                    new_level_id = level.id
                    return redirect("cafe:level_view", new_level_id)
                except msgspec.ValidationError:
                    messages.error(request, "An error occurred validating the level")
            else:
                messages.error(request, "An error occurred validating the form")
        if prefill.prefill_type == 'update':
            # we're updating a level. The level ID is provided by the client in the "prefill" form property.
            form = PrefillStageTwoPayload(request.POST)
            if form.is_valid():
                prefill_data: str = form.cleaned_data.get("prefill")
                try:
                    parsed = msgspec.json.decode(prefill_data, type=dict)
                    level_id = parsed.get("level_id")
                    level = get_object_or_404(RDLevel, pk=level_id)
                    if not request.user.has_perm('cafe.change_rdlevel', level):
                        messages.error(request, "You do not have permission to edit this level")
                    else:
                        for key, value in prefill.data.items():
                            setattr(level, key, value)
                        with transaction.atomic():
                            level.save()
                            prefill.delete()
                        return redirect("cafe:level_view", level.id)
                except msgspec.ValidationError:
                    messages.error(request, "An error occurred validating the level")
            else:
                messages.error(request, "An error occurred validating the form")

    potential_matches = []
    if prefill.prefill_type == 'update':
        matches = RDLevel.objects.filter(song_raw=prefill.data['song_raw'], artist_raw=prefill.data['artist_raw'])
        potential_matches.extend(match for match in matches if request.user.has_perm('cafe.change_rdlevel', match))

    render_data = {
        "prefill": prefill.to_dict(),
        "potential_matches": [m.to_dict() for m in potential_matches]
    }
    return Response(request, request.resolver_match.view_name, render_data)