from cafe.views.types import HttpRequest
from django.contrib import messages
from django.shortcuts import redirect, render

def login(request: HttpRequest):
    next_url = request.GET.get("next")
    if next_url and request.user.is_authenticated:
        # there is a redirect, but the user is already authenticated.
        # therefore, the user does not have permissions to do the action.
        # set a message up and redirect back to home.
        messages.add_message(request, messages.ERROR, "You do not have permissions to perform that action")
        return redirect("cafe:index")
    if not request.user.is_authenticated:
        # the user is not authenticated.
        # therefore, the user should be redirected to discord login.
        return render(request, "cafe/login.html", {"next": next_url})
    if request.user.is_authenticated:
        # the user is authenticated but there's no next param.
        # how did they get here?
        return redirect("cafe:index")