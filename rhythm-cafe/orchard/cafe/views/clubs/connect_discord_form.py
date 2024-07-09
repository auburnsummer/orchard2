from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core.signing import TimestampSigner, BadSignature
from django.utils.decorators import method_decorator

from django.views import View
from django.forms import Form

from datetime import timedelta

from cafe.models import ClubMembership

connectgroup_signer = TimestampSigner(salt="connectgroup")

class ConnectDiscordForm(Form):
    pass

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
        breakpoint()

connect_discord_form = ConnectDiscordFormView.as_view()