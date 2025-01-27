from django.forms import ModelForm
from django.urls import reverse
from django.http import HttpResponseForbidden, HttpResponseServerError, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from rules.contrib.views import permission_required, objectgetter
from django.utils.crypto import get_random_string
import string

from cafe.models import Club
from cafe.models.clubs.club_invite import ClubInvite

from django.utils import timezone
from datetime import timedelta

from urllib.parse import urlencode

class CreateInviteForm(ModelForm):
    class Meta:
        model = ClubInvite
        fields = ["role"]

@permission_required("cafe.create_invite_for_club", fn=objectgetter(Club, 'club_id'))
def create_invite(request, club_id):
    if request.method != "POST":
        return HttpResponseForbidden()

    form = CreateInviteForm(request.POST)
    if form.is_valid():
        role = form.cleaned_data.get("role")
        new_invite = ClubInvite(
            club = get_object_or_404(Club, pk=club_id),
            role = role,
            expiry = timezone.now() + timedelta(hours=24),
            code = role + "_" + get_random_string(30, string.ascii_letters)
        )
        new_invite.save()
        qs = "?" + urlencode({
            "invite_code": new_invite.code
        })
        return HttpResponseRedirect(reverse('club_settings_members', args=[club_id]) + qs)

    return HttpResponseServerError()
