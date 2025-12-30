from django import forms
from django.shortcuts import get_object_or_404, redirect
from django_bridge.response import Response

from cafe.models.clubs.club import Club
from cafe.models.rdlevels.rdlevel import RDLevel

from rules.contrib.views import permission_required, objectgetter
from django.contrib import messages

from orchard.settings import STEWARD_CLUB_ID

class ClubDeleteForm(forms.Form):
    level_action = forms.CharField()

@permission_required("cafe.delete_club", fn=objectgetter(Club, 'club_id'))
def club_delete(request, club_id):
    club = get_object_or_404(Club, pk=club_id)

    if request.method == "POST":
        form = ClubDeleteForm(request.POST)
        if not form.is_valid():
            messages.error(request, "Invalid form submission.")
            return redirect("cafe:club_delete", club_id=club_id)
        level_action = form.cleaned_data["level_action"]
        if level_action == "delete":
            club.delete() # Cascade will handle associated levels.
        elif level_action == "disassociate":
            # all levels move to csteward
            steward_club = Club.objects.get(id=STEWARD_CLUB_ID)
            levels = RDLevel.objects.filter(club=club)
            levels.update(club=steward_club)
            club.delete()
        else:
            messages.error(request, "Invalid level handling option.")
            return redirect("cafe:club_delete", club_id=club_id)
        messages.success(request, "Group deleted successfully.")
        return redirect("cafe:profile_clubs")

    club_level_count = RDLevel.objects.filter(club=club).count()

    props = {
        "club": club.to_dict(),
        "club_level_count": club_level_count,
    }

    return Response(request, request.resolver_match.view_name, props)
