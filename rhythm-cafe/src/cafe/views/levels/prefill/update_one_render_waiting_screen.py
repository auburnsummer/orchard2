from rules.contrib.views import permission_required

from django.shortcuts import render

from cafe.models.rdlevel import RDLevel
from cafe.models.user import User

def get_levels_user_can_update(user: User):
    # users can update their own levels
    own_levels = user.rdlevel_set.all()

    # users can update levels that they're admins of
    admin_clubs = user.memberships.filter(role__exact="admin")

    
    return own_levels

@permission_required('prefill.ok', fn=lambda _, code: code)
def update_one_select_level(request, code):
    """
    Stage 1: Render a screen for the user to select the level to update.

    In the background, the user's browser will call Stage 2 via AJAX to get the upload going.
    """
    render_data = {
        "code": code
    }
    
    return render(request, "cafe/levels/update.jinja", render_data)
