from django import forms
from django.http import JsonResponse
from cafe.models.rdlevels.daily_blend_configuration import DailyBlendConfiguration
from cafe.views.types import HttpRequest
from rules.contrib.views import permission_required

from cafe.bridge.response import Response

from django.contrib import messages

class BlendConfigForm(forms.ModelForm):
    class Meta:
        model = DailyBlendConfiguration
        fields = ["webhook_urls", "jsonata_script", "paused", "reporting_webhook_url"]


@permission_required('cafe.blend_rdlevel')
def blend_config(request: HttpRequest) -> JsonResponse:
    config = DailyBlendConfiguration.get_config()

    if request.method == "POST":
        form = BlendConfigForm(request.POST, instance=config)
        if form.is_valid():
            form.save()
            messages.success(request, "Configuration updated successfully.")
        else:
            messages.error(request, "Invalid form submission.")

    return Response(request, request.resolver_match.view_name, {
        "config": config.to_dict()
    })