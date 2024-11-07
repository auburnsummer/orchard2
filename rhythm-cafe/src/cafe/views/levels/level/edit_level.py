import json
import rules

from rules.contrib.views import permission_required, objectgetter

from django.shortcuts import render
from cafe.models.rdlevel import RDLevel
from django.forms.models import model_to_dict

from django.core.serializers.json import DjangoJSONEncoder

@permission_required('cafe.change_rdlevel', fn=objectgetter(RDLevel, 'level_id'))
def edit_level(request, level_id):
    level = RDLevel.objects.get(id=level_id)

    dict = model_to_dict(level)
    serialized = json.dumps(dict, cls=DjangoJSONEncoder)

    def has_permission(perm):
        return rules.has_perm(perm, request.user, level)
    
    payload = {
        "has_permission": has_permission,
        "level": level,
        "clubs": []
    }
    return render(request, 'cafe/levels/view_level.jinja', payload)