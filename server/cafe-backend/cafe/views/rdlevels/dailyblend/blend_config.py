from django import forms
from django.http import JsonResponse
from cafe.models.rdlevels.daily_blend_configuration import DailyBlendConfiguration
from cafe.tasks.report_blend_change import blend_paused, jsonata_changed, report_blend_change, reporting_url_changed, webhook_urls_changed
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
            if "paused" in form.changed_data:
                report_blend_change(blend_paused(config.paused, request.user))
            if "webhook_urls" in form.changed_data:
                report_blend_change(webhook_urls_changed(form.initial["webhook_urls"], form.cleaned_data["webhook_urls"], request.user))
            if "jsonata_script" in form.changed_data:
                report_blend_change(jsonata_changed(form.initial["jsonata_script"], form.cleaned_data["jsonata_script"], request.user))
            if "reporting_webhook_url" in form.changed_data:
                report_blend_change(reporting_url_changed(form.cleaned_data["reporting_webhook_url"], request.user), override_webhook_url=form.initial["reporting_webhook_url"])
            messages.success(request, "Configuration updated successfully.")
        else:
            messages.error(request, "Invalid form submission.")

    return Response(request, request.resolver_match.view_name, {
        "config": config.to_dict()
    })