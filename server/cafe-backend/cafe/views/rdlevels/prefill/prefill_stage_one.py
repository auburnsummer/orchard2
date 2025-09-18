from allauth.account.decorators import login_required
from django.forms import CharField, Form
from django.http import HttpResponseRedirect
from django.urls import reverse
from rules.contrib.views import permission_required
from django_bridge.response import Response
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

@permission_required('prefill.ok', fn=lambda _, code: code)
def _prefill_stage_one_post(request: AuthenticatedHttpRequest, code: str):
    """Handle POST request with permission check"""
    form = PrefillStageOneForm(request.POST)
    if form.is_valid():
        prefill_type = form.cleaned_data["prefill_type"]
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
            version=1,
            user=user,
            prefill_type=prefill_type,
            club=club
        )
        run_prefill(rdlevel_prefill_result.id)
        return HttpResponseRedirect(reverse("cafe:level_from_prefill", args=[rdlevel_prefill_result.id]))

@login_required
def prefill_stage_one(request: AuthenticatedHttpRequest, code: str):
    if request.method == "POST":
        return _prefill_stage_one_post(request, code)

    render_data = {
        "code": code,
        "code_valid": request.user.has_perm("prefill.ok", code)
    }
    
    return Response(request, request.resolver_match.view_name, render_data)
