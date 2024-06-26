from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
from django.contrib import messages
from cafe.models import User


class ProfileInfoForm(ModelForm):
    class Meta:
        model = User
        fields = ["first_name"]

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileInfoForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            request.user.first_name = form.cleaned_data.get("first_name")
            request.user.save()
            messages.add_message(request, messages.SUCCESS, f"Name changed to {request.user.first_name}.")

            return HttpResponseRedirect("/accounts/profile")
    else:
        form = ProfileInfoForm(initial={'first_name': request.user.first_name})

    return render(request, "cafe/profile/profile.jinja")
