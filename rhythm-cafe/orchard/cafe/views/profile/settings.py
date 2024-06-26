from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
from cafe.models import UserProfile

from django.contrib import messages

class ProfileUserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ["theme_pref"]

@login_required
def settings(request):
    if request.method == 'POST':
        form = ProfileUserProfileForm(request.POST)
        if form.is_valid():
            user_prof = request.user.profile
            user_prof.theme_pref = form.cleaned_data.get("theme_pref")
            user_prof.save()
            messages.add_message(request, messages.SUCCESS, "Settings changed")
            return HttpResponseRedirect("/accounts/profile/settings")

    return render(request, "cafe/profile/settings.jinja")
