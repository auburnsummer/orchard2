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

class EditRDlevelPayload(forms.Form):
    prefill = forms.CharField()


@permission_required('cafe.change_rdlevel', fn=objectgetter(RDLevel, attr_name="level_id"))
def edit_rdlevel(request: AuthenticatedHttpRequest, level_id: str):
    rdlevel = get_object_or_404(RDLevel, id=level_id)
    if request.method == 'POST':
        form = EditRDlevelPayload(request.POST)
        if form.is_valid():
            prefill_data: str = form.cleaned_data.get("prefill")
            try:
                parsed = msgspec.json.decode(prefill_data, type=AddLevelPayload)
                for key, value in msgspec.structs.asdict(parsed).items():
                    setattr(rdlevel, key, value)

                with transaction.atomic():
                    rdlevel.save()

                return redirect("cafe:level_view", rdlevel.id)
            except msgspec.ValidationError as e:
                messages.error(request, "An error occurred validating the level")
        else:
            messages.error(request, "An error occurred validating the form")


    props = {
        "rdlevel": rdlevel.to_dict()
    }
    return Response(request, request.resolver_match.view_name, props)