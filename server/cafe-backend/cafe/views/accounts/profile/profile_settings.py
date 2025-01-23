from allauth.account.decorators import login_required
from django_bridge.response import Response

from django.forms import ModelForm
from django.contrib import messages
from django.http import HttpResponse

from cafe.models.user import User
from cafe.views.types import AuthenticatedHttpRequest

class PostSettingsForm(ModelForm):
    class Meta:
        model = User
        fields = ["display_name", "theme_preference"]

@login_required
def settings(request: AuthenticatedHttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = PostSettingsForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            for field, value in form.cleaned_data.items():
                setattr(request.user, field, value)
            request.user.save()
            messages.add_message(request, messages.SUCCESS, f"User updated!")

    return Response(request, request.resolver_match.view_name, {})