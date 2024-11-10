import json
from django.http import HttpResponseBadRequest, JsonResponse
from django.urls import reverse
import rules

from rules.contrib.views import permission_required, objectgetter

from django.shortcuts import render
from cafe.models.rdlevel import RDLevel
from django.forms.models import model_to_dict
from django_minify_html.decorators import no_html_minification

from django.core.serializers.json import DjangoJSONEncoder

import msgspec
from cafe.views.levels.level.common import AddLevelPayload

def edit_level_post(request, level: RDLevel):
    try:
        body = msgspec.json.decode(request.body, type=AddLevelPayload)
        for field in msgspec.structs.fields(AddLevelPayload):
            setattr(level, field.name, getattr(body, field.name))
        level.save()

        payload = {
            "id": level.id,
            "url": reverse("cafe:level_view", args=[level.id])
        }

        return JsonResponse(payload)
    except msgspec.ValidationError as e:
        # return 401 error response
        return HttpResponseBadRequest(str(e))


def edit_level_get(request, level: RDLevel):
    dict = model_to_dict(level)
    serialized = json.dumps(dict, cls=DjangoJSONEncoder)
    
    render_data = {
        "prefill": serialized,
        "club": level.club,
        "mode": "edit"
    }
    return render(request, 'cafe/levels/edit_level.jinja', render_data)

@permission_required('cafe.change_rdlevel', fn=objectgetter(RDLevel, 'level_id'))
def edit_level(request, level_id):
    level = RDLevel.objects.get(id=level_id)
    if request.method == 'POST':
        return edit_level_post(request, level)
    else:
        return edit_level_get(request, level)