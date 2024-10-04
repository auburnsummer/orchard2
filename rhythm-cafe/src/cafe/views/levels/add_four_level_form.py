from django.shortcuts import get_object_or_404, render
from cafe.models import RDLevelPrefillResult

from django.contrib.auth.decorators import login_required
from django_minify_html.decorators import no_html_minification

from rules.contrib.views import permission_required, objectgetter

@no_html_minification
@permission_required('prefill.can_access_prefill', fn=objectgetter(RDLevelPrefillResult, 'prefill_id'))
@login_required
def add_four_level_form(request, prefill_id):
    "Stage 4: This is the form that the user fills out, and then submits."
    prefill = get_object_or_404(RDLevelPrefillResult, id=prefill_id)
    render_data = {
        "prefill": prefill.data.decode("utf-8"),
        "club": prefill.club
    }
    return render(request, "cafe/levels/after_prefill.jinja", render_data)