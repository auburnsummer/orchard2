from django.shortcuts import get_object_or_404, render
from cafe.models import RDLevelPrefillResult

from django.contrib.auth.decorators import login_required
from django_minify_html.decorators import no_html_minification

@no_html_minification
@login_required
def add_four_level_form(request, prefill_id):
    "Stage 4: This is the form that the user fills out, and then submits."
    prefill = get_object_or_404(RDLevelPrefillResult, id=prefill_id)
    render_data = {
        "result": prefill.data.decode("utf-8")
    }
    return render(request, "cafe/levels/after_prefill.jinja", {
        "prefill": render_data
    })