from cafe.bridge.response import Response

from django.forms import ModelForm
from django.contrib import messages
from django.http import HttpResponse

from cafe.models.user import User
from cafe.views.types import HttpRequest

class PostSettingsForm(ModelForm):
    class Meta:
        model = User
        fields = ["display_name", "theme_preference"]

def settings(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = PostSettingsForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            if request.user.is_authenticated:
                # save it on the user
                for field, value in form.cleaned_data.items():
                    setattr(request.user, field, value)
                request.user.save()
                messages.add_message(request, messages.SUCCESS, "User updated!")

            else:
                # save it on the session
                for field, value in form.cleaned_data.items():
                    request.session[field] = value
                messages.add_message(request, messages.SUCCESS, "Settings updated!")
        else:
            messages.add_message(request, messages.ERROR, "Invalid form")

    view_name = request.resolver_match.view_name if request.resolver_match else ""
    return Response(request, view_name, {})