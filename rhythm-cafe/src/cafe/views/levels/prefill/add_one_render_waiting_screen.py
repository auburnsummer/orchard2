from rules.contrib.views import permission_required

from django.shortcuts import render

# we are importing this as a side effect, as it will register the prefill.ok permission
# this dance is to avoid the type checker complaining about the unused import
from . import check
assert check
del check

@permission_required('prefill.ok', fn=lambda _, code: code)
def add_one_render_waiting_screen(request, code):
    "Stage 1: Render the 'Analyzing level' screen. The screen calls Stage 2 via AJAX."
    render_data = {
        "code": code
    }
    
    return render(request, "cafe/levels/add.jinja", render_data)
