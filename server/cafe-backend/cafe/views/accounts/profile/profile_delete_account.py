from allauth.account.decorators import login_required
from django import forms
from django.shortcuts import redirect
from django_bridge.response import Response

from cafe.models.clubs.club import Club
from cafe.models.clubs.club_membership import ClubMembership
from cafe.models.rdlevels.rdlevel import RDLevel
from cafe.models.user import User
from cafe.views.types import AuthenticatedHttpRequest
from orchard.settings import STEWARD_USER_ID

from django.contrib import messages

class DeleteAccountForm(forms.Form):
    level_handling = forms.CharField()
    

@login_required
def profile_delete_account(request: AuthenticatedHttpRequest):
    user = request.user

    if request.method == "POST":
        form = DeleteAccountForm(request.POST)
        if form.is_valid():
            level_handling = form.cleaned_data["level_handling"]
            if level_handling == "delete":
                user.delete() # Delete cascade will handle associated levels.
                messages.success(request, "Your account has been deleted.")
            elif level_handling == "transfer":
                steward = User.objects.get(username=STEWARD_USER_ID)
                if not steward:
                    raise Exception("Steward user does not exist.")
                levels = RDLevel.objects.filter(submitter=user)
                levels.update(submitter=steward)
                user.delete()
                messages.success(request, "Your account has been deleted.")
            return redirect("cafe:index")
        else:
            messages.error(request, "Invalid form submission.")

    levels = RDLevel.objects.filter(submitter=user)
    number_of_levels = levels.count()

    club_memberships = ClubMembership.objects.filter(user=user, role="owner")
    number_of_clubs = club_memberships.count()
    
    return Response(request, request.resolver_match.view_name, {
        "number_of_levels": number_of_levels,
        "number_of_clubs": number_of_clubs,
    })