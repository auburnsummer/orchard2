from allauth.account.decorators import login_required
from django_bridge.response import Response

from django.forms import ModelForm
from django.contrib import messages

from cafe.models.user import User

class PostSettingsForm(ModelForm):
    class Meta:
        model = User
        fields = ["display_name"]


@login_required
def settings(request):
    if request.method == "POST":
        form = PostSettingsForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            for field, value in form.cleaned_data.items():
                setattr(request.user, field, value)
            request.user.save()
            messages.add_message(request, messages.SUCCESS, f"User updated!")
    return Response(request, "Profile", {"subpage": "settings"})