import msgspec
from django import forms
from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django_bridge.response import Response
from rules.contrib.views import objectgetter, permission_required

from cafe.models import RDLevel
from cafe.views.rdlevels.common import AddLevelPayload
from cafe.views.types import AuthenticatedHttpRequest



@permission_required('cafe.delete_rdlevel', fn=objectgetter(RDLevel, attr_name="level_id"))
def delete_rdlevel(request: AuthenticatedHttpRequest, level_id: str):
    rdlevel = get_object_or_404(RDLevel, id=level_id)
    if request.method == 'POST':
        rdlevel.delete()
        messages.success(request, "Successfully deleted level")

    return redirect("cafe:index")