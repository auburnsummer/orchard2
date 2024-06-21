from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.forms import ModelForm
from django.db import transaction
from rules.contrib.views import permission_required, objectgetter

from django.urls import reverse

from cafe.models import ClubMembership

class AlterMembershipForm(ModelForm):
    class Meta:
        model = ClubMembership
        fields = ["role"]

def get_membership_by_club_and_user(_, club_id, user_id):
    return get_object_or_404(ClubMembership, user=user_id, club=club_id)

@permission_required("cafe.change_clubmembership", fn=get_membership_by_club_and_user)
def alter_membership(request, club_id, user_id):
    if request.method != 'POST':
        return HttpResponseForbidden()

    form = AlterMembershipForm(request.POST)
    if form.is_valid():
        membership = get_object_or_404(ClubMembership, user=user_id, club=club_id)
        
        owners = list(ClubMembership.objects.filter(club=club_id, role="owner"))
        if len(owners) < 2 and form.cleaned_data.get("role") != "owner" and membership.role == "owner":
            return HttpResponseForbidden("Cannot demote this user as it would result in the group having no owners")

        membership.role = form.cleaned_data.get("role")
        membership.save()

    return HttpResponseRedirect(reverse("cafe:club_settings_members", args=[club_id]))

@permission_required("cafe.delete_clubmembership", fn=get_membership_by_club_and_user)
def delete_membership(request, club_id, user_id):
    if request.method != 'POST':
        return HttpResponseForbidden()
    

    owners = list(ClubMembership.objects.filter(club=club_id, role="owner"))
    if len(owners) < 2:
        return HttpResponseForbidden("Cannot kick this user as it would result in the group having no owners")
    
    membership = get_object_or_404(ClubMembership, user=user_id, club=club_id)
    membership.delete()

    return HttpResponseRedirect(reverse("cafe:club_settings_members", args=[club_id]))
