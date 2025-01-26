from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.forms import ModelForm
from django_bridge.response import Response
from rules.contrib.views import permission_required

from django.urls import reverse
from cafe.models import ClubMembership
from cafe.views.types import AuthenticatedHttpRequest
from django.contrib import messages

class AlterMembershipForm(ModelForm):
    class Meta:
        model = ClubMembership
        fields = ["role"]

# this is used for the permission_required fn decorator
def get_membership_by_club_and_user(_: AuthenticatedHttpRequest, club_id: str, user_id: str):
    return get_object_or_404(ClubMembership, user=user_id, club=club_id)

@permission_required("cafe.change_clubmembership", fn=get_membership_by_club_and_user)
def alter_membership(request: AuthenticatedHttpRequest, club_id: str, user_id: str):
    if request.method != 'POST':
        return HttpResponseForbidden()

    form = AlterMembershipForm(request.POST)
    if form.is_valid():
        membership = get_object_or_404(ClubMembership, user=user_id, club=club_id)
        
        owners = list(ClubMembership.objects.filter(club=club_id, role="owner"))
        if len(owners) < 2 and form.cleaned_data.get("role") != "owner" and membership.role == "owner":
            messages.add_message(request, messages.WARNING, "Cannot demote this user as it would result in the group having no owners")
        else:
            membership.role = form.cleaned_data.get("role")
            membership.save()
            messages.add_message(request, messages.SUCCESS, "Member role changed successfully.")

    return redirect("club_settings_members", club_id=club_id)

@permission_required("cafe.delete_clubmembership", fn=get_membership_by_club_and_user)
def delete_membership(request: AuthenticatedHttpRequest, club_id: str, user_id: str):
    if request.method != 'POST':
        return HttpResponseForbidden()

    owners = list(ClubMembership.objects.filter(club=club_id, role="owner"))
    membership = get_object_or_404(ClubMembership, user=user_id, club=club_id)

    if len(owners) < 2 and membership.role == "owner":
        messages.add_message(request, messages.WARNING, "Cannot kick this user as it would result in the group having no owners")
    else:    
        membership.delete()
        messages.add_message(request, messages.SUCCESS, "Member removed from group successfully.")

    # if the membership that was just deleted was the user, redirect to home instead.
    if user_id == request.user.id:
        return redirect("index")

    return redirect("club_settings_members", club_id=club_id)
