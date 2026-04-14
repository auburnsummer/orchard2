from allauth.account.decorators import login_required
from django.shortcuts import redirect

from cafe.views.types import AuthenticatedHttpRequest


@login_required
def profile_levels(request: AuthenticatedHttpRequest):
    user = request.user
    return redirect(f"/levels/?q=&submitter_id={user.id}&peer_review=all&show_hidden=all")
