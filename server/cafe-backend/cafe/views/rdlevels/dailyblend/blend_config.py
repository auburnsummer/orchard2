from django import forms
from django.http import JsonResponse
from cafe.models.rdlevels.daily_blend_configuration import DailyBlendConfiguration
from cafe.views.types import HttpRequest
from rules.contrib.views import permission_required

from django_bridge.response import Response

from django.contrib import messages

class BlendConfigForm(forms.Form):
    webhook_urls = forms.CharField(required=False)
    jsonata_script = forms.CharField(required=False)

@permission_required('cafe.blend_rdlevel')
def blend_config(request: HttpRequest) -> JsonResponse:
    config = DailyBlendConfiguration.get_config()

    if request.method == "POST":
        form = BlendConfigForm(request.POST)
        if form.is_valid():
            config.webhook_urls = form.cleaned_data['webhook_urls']
            config.jsonata_script = form.cleaned_data['jsonata_script']
            config.save()
            messages.success(request, "Configuration updated successfully.")
        else:
            messages.error(request, "Invalid form submission.")

    return Response(request, request.resolver_match.view_name, {
        "config": config.to_dict()
    })