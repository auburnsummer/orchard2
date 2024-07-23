from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed

from .check import check_if_ok_to_continue

from huey.contrib.djhuey import db_task
from cafe.views.discord_bot.handlers.add import addlevel_signer
from vitals import vitals

from cafe.models import Club

import httpx


@db_task()
def _run_prefill(level_url, club_id, user):
    club = Club.objects.get(id=club_id)
    
    pass


@login_required
def prefill(request, code):
    if request.method != "POST":
        return HttpResponseNotAllowed()

    check_if_ok_to_continue(code, request.user)

    result = addlevel_signer.unsign_object(code)
    level_url = result['level_url']
    club_id = result['club_id']
    _run_prefill(level_url, club_id, request.user)