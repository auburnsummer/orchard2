from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.signing import TimestampSigner, BadSignature
from django.urls import reverse
from django.utils.decorators import method_decorator

from django.core.exceptions import PermissionDenied, BadRequest

from django.views import View
from django.forms import Form, CharField

from datetime import timedelta
from django.contrib import messages

from cafe.models import ClubMembership, DiscordGuild

connectgroup_signer = TimestampSigner(salt="connectgroup")

class ConnectDiscordForm(Form):
    club_id = CharField(max_length=100)

class ConnectDiscordFormView(View):
    @method_decorator(login_required)
    def get(self, request, code):
        try:
            result = connectgroup_signer.unsign(code, max_age=timedelta(days=3))
        except (BadSignature, ValueError):
            result = None

        clubs = [cm.club for cm in ClubMembership.objects.filter(user=request.user, role='owner')]

        render_data = {
            "guild_id": result,
            "clubs": clubs
        }

        return render(request, "cafe/clubs/connect_discord_form.jinja", render_data)

    @method_decorator(login_required)
    def post(self, request, code):
        try:
            guild_id = connectgroup_signer.unsign(code, max_age=timedelta(days=3))
        except (BadSignature, ValueError):
            raise PermissionDenied("Code invalid")

        form = ConnectDiscordForm(request.POST)
        if not form.is_valid():
            raise BadRequest("Form not valid")

        club_id = form.cleaned_data.get('club_id')
        try:
            # just verifying it exists
            membership = ClubMembership.objects.get(user=request.user, club__id=club_id, role='owner')
            club = membership.club
        except ClubMembership.DoesNotExist:
            raise PermissionDenied("User is not an owner of the group")
        
        # we're good to go from here.
        discord_guild, _ = DiscordGuild.objects.get_or_create(id=guild_id)
        discord_guild.club = club
        discord_guild.save()

        messages.add_message(request, messages.SUCCESS, "Discord server linked")

        return HttpResponseRedirect(reverse('cafe:club_settings_info', args=[club_id]))

connect_discord_form = ConnectDiscordFormView.as_view()