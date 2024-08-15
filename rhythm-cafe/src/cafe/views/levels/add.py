from cafe.views.discord_bot.handlers.add import addlevel_signer

from django.core.signing import BadSignature

from django.core.exceptions import BadRequest, ObjectDoesNotExist

from datetime import timedelta

from cafe.models import Club
from rules.contrib.views import permission_required
from oauthlogin.models import OAuthConnection
from cafe.models.club import is_at_least_admin

from django.shortcuts import render

from .check import check_if_ok_to_continue



@permission_required('prefill.ok', fn=lambda _, code: code)
def add(request, code):    
    render_data = {
        "code": code
    }
    
    return render(request, "cafe/levels/add.jinja", render_data)
