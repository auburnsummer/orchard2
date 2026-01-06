from allauth.account.decorators import login_required
from django.forms import BooleanField, CharField, Form
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse
from rules.contrib.views import permission_required
from django_bridge.response import Response
from vitals.vitals import PREFILL_VERSION
from .predicates import register_permissions

from cafe.views.types import AuthenticatedHttpRequest

from cafe.models.rdlevels.prefill import RDLevelPrefillResult
from cafe.views.discord_bot.handlers.add import addlevel_signer
from cafe.models.rdlevels.tempuser import get_or_create_discord_user
from cafe.models.clubs.club import Club
from django.utils.timezone import timedelta
from django.shortcuts import get_object_or_404

from cafe.tasks.run_prefill import run_prefill

register_permissions()

class PrefillStageOneForm(Form):
    prefill_type = CharField(max_length=100)
    go_to_prepost = BooleanField(required=False, initial=False)

@permission_required('prefill_code.ok', fn=lambda _, code: code)
def _prefill_stage_one_post(request: AuthenticatedHttpRequest, code: str):
    """Handle POST request with permission check"""
    form = PrefillStageOneForm(request.POST)
    if form.is_valid():
        prefill_type = form.cleaned_data["prefill_type"]
        go_to_prepost = form.cleaned_data["go_to_prepost"]
        # we don't need to check again if this is valid because the permission check would have failed if it's not.
        result = addlevel_signer.unsign_object(code, max_age=timedelta(days=1))
        discord_user_id = result['discord_user_id']
        discord_user_name_hint = result['discord_user_name_hint']
        user = get_or_create_discord_user(discord_user_id, discord_user_name_hint)
        level_url = result['level_url']
        club_id = result['club_id']
        club = get_object_or_404(Club, id=club_id)
        rdlevel_prefill_result = RDLevelPrefillResult.objects.create(
            url=level_url,
            version=PREFILL_VERSION,
            user=user,
            prefill_type=prefill_type,
            club=club,
            go_to_prepost=go_to_prepost
        )
        run_prefill(rdlevel_prefill_result.id)
        return HttpResponseRedirect(reverse("cafe:level_from_prefill", args=[rdlevel_prefill_result.id]))
    else:
        return HttpResponseBadRequest()

@login_required
def prefill_stage_one(request: AuthenticatedHttpRequest, code: str):
    if request.method == "POST":
        return _prefill_stage_one_post(request, code)

    render_data = {
        "code": code,
        "code_valid": request.user.has_perm("prefill_code.ok", code)
    }
    
    return Response(request, request.resolver_match.view_name, render_data)
