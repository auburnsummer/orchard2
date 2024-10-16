
from django.shortcuts import render
from cafe.models.rdlevel import RDLevel


def view_level(request, level_id):
    level = RDLevel.objects.get(id=level_id)
    return render(request, 'cafe/levels/view_level.jinja', {'level': level})