from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.forms import ModelForm, CharField, ValidationError
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from django.utils.http import url_has_allowed_host_and_scheme
from django_bridge.response import Response
from cafe.models import Club, ClubMembership
from orchard.settings import DOMAIN_URL

from cafe.views.types import AuthenticatedHttpRequest

class CreateClubForm(ModelForm):
    redirect = CharField(required=False)

    class Meta:
        model = Club
        fields = ["name"]

    def clean_redirect(self):
        url = self.cleaned_data.get("redirect")
        if url and not url_has_allowed_host_and_scheme(
            url=url,
            allowed_hosts={DOMAIN_URL.replace("https://", "").replace("http://", "")},
            require_https=DOMAIN_URL.startswith("https://"),
        ):
            raise ValidationError("Invalid redirect URL.")
        return url

@login_required
@transaction.atomic
def create_club(request: AuthenticatedHttpRequest):
    if request.method == 'POST':
        form = CreateClubForm(request.POST)
        if form.is_valid():
            new_club = Club(
                name=form.cleaned_data.get("name")
            )
            # add current user as owner
            current_user_membership = ClubMembership(
                user=request.user,
                club=new_club,
                role='owner'
            )
            new_club.save()
            current_user_membership.save()

            messages.success(request, "Group created!")

            return HttpResponseRedirect(form.cleaned_data.get("redirect") or f"/groups/{new_club.id}/settings")

    return Response(request, request.resolver_match.view_name, {}, overlay=True)