from django.shortcuts import render, get_object_or_404
from django_bridge.response import Response
from rules.contrib.views import permission_required, objectgetter

from cafe.models import Club

from django.views import View
from django.utils.decorators import method_decorator
from django.forms import ModelForm

from django.contrib import messages


class ClubInfoForm(ModelForm):
    class Meta:
        model = Club
        fields = ["name"]


class ClubSettingsInfoView(View):
    @method_decorator(permission_required('cafe.view_info_of_club', fn=objectgetter(Club, 'club_id')))
    def get(self, request, club_id):
        club = get_object_or_404(Club, pk=club_id)

        render_data = {
            "club": club.to_dict()
        }
        return Response(request, "ClubSettingsInfo", render_data)
    
    @method_decorator(permission_required('cafe.change_info_of_club', fn=objectgetter(Club, 'club_id')))
    def post(self, request, club_id):
        form = ClubInfoForm(request.POST)
        club = get_object_or_404(Club, pk=club_id)
        if form.is_valid():
            club.name = form.cleaned_data.get("name")
            club.save()
            messages.add_message(request, messages.SUCCESS, f"Group update successful")

        render_data = {
            "club": club.to_dict()
        }
        return Response(request, "ClubSettingsInfo", render_data)

info = ClubSettingsInfoView.as_view()