from rules.contrib.views import permission_required

from django.shortcuts import render


@permission_required('prefill.ok', fn=lambda _, code: code)
def add_one_render_waiting_screen(request, code):
    "Stage 1: Render the 'Analyzing level' screen. The screen calls Stage 2 via AJAX."
    render_data = {
        "code": code
    }
    
    return render(request, "cafe/levels/add.jinja", render_data)
