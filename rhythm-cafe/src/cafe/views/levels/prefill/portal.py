from rules.contrib.views import permission_required

from django.shortcuts import render


@permission_required('prefill.ok', fn=lambda _, code: code)
def portal(request, code):
    "Stage 0: Render the screen that asks the user to choose if it's a new level or an update to an existing level."
    render_data = {
        "code": code
    }
    
    return render(request, "cafe/levels/portal.jinja", render_data)
