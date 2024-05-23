from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm

from cafe.models import User

from django.forms import widgets

from oauthlogin.providers import get_provider_keys


@login_required
def connections(request):
    render_data = {
        "user": request.user,
        "oauth_provider_keys": get_provider_keys()
    }

    return render(request, "cafe/profile/connections.jinja", render_data)
