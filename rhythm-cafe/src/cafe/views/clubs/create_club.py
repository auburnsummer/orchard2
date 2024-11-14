from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.forms import ModelForm
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from cafe.models import Club, ClubMembership

class CreateClubForm(ModelForm):
    class Meta:
        model = Club
        fields = ["name"]

@login_required
@transaction.atomic
def create_club(request):
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

            messages.success(request, "Club created!")

            return HttpResponseRedirect(f"/groups/{new_club.id}/settings")

    return render(request, "cafe/clubs/create_club.jinja")
