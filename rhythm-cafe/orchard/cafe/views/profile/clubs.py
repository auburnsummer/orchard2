from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
from cafe.models import User


@login_required
def clubs(request):
    roles = ["owner", "admin"]

    memberships = { role: request.user.clubmembership_set.filter(role__exact=role) for role in roles}

    render_data = {
        "memberships": memberships,
    }

    return render(request, "cafe/profile/clubs.jinja", render_data)
