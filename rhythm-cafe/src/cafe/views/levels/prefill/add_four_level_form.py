from http.client import HTTPResponse
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render
from cafe.models import RDLevelPrefillResult, RDLevel, ClubRDLevel

from django.contrib.auth.decorators import login_required
from django_minify_html.decorators import no_html_minification

from rules.contrib.views import permission_required, objectgetter

from vitals.msgspec_schema import VitalsLevelBaseMutable

import msgspec
import json

class AddLevelPayload(VitalsLevelBaseMutable):
    song_alt: str

def add_level_route(request, prefill: RDLevelPrefillResult):
    try:
        body = msgspec.json.decode(request.body, type=AddLevelPayload)
        args = {
            **prefill.data,
            **msgspec.structs.asdict(body),
            "submitter": prefill.user
        }
        
        new_level = RDLevel(**args)
        new_level.save()

        club_rd_level = ClubRDLevel(
            rdlevel=new_level,
            club=prefill.club
        )
        club_rd_level.save()

        # todo: should probably contain a redirect to the level instead
        return HTTPResponse("Success")
    except msgspec.ValidationError as e:
        # return 401 error response
        return HttpResponseBadRequest(str(e))
    pass

@no_html_minification
@permission_required('prefill.can_access_prefill', fn=objectgetter(RDLevelPrefillResult, 'prefill_id'))
@login_required
def add_four_level_form(request, prefill_id):
    "Stage 4: This is the form that the user fills out, and then submits."
    prefill = get_object_or_404(RDLevelPrefillResult, id=prefill_id)
    if request.method == 'POST':
        return add_level_route(request, prefill)
    else:
        render_data = {
            "prefill": json.dumps(prefill.data),
            "club": prefill.club
        }
        return render(request, "cafe/levels/after_prefill.jinja", render_data)