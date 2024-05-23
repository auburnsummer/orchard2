from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm

from cafe.models import User

from django.forms import widgets

class ShoelaceTextWidget(widgets.TextInput):
    def render(self, name, value, attrs = ..., renderer = ...):
        return super().render(name, value, attrs, renderer)

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
            return HttpResponseRedirect("/accounts/profile")
    else:
        form = ProfileInfoForm(initial={'first_name': request.user.first_name})

    return render(request, "cafe/profile/profile.jinja", { "user": request.user })
