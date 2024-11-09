import json
import rules

from rules.contrib.views import permission_required, objectgetter

from django.shortcuts import render
from cafe.models.rdlevel import RDLevel
from django.forms.models import model_to_dict
from django_minify_html.decorators import no_html_minification

from django.core.serializers.json import DjangoJSONEncoder

@permission_required('cafe.change_rdlevel', fn=objectgetter(RDLevel, 'level_id'))
def edit_level(request, level_id):
    level = RDLevel.objects.get(id=level_id)

    dict = model_to_dict(level)
    serialized = json.dumps(dict, cls=DjangoJSONEncoder)

    print(serialized)
    
    render_data = {
        "prefill": serialized,
        "club": level.club,
        "mode": "edit"
    }
    return render(request, 'cafe/levels/edit_level.jinja', render_data)