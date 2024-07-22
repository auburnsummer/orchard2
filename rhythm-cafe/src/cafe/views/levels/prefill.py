from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed



@login_required
def prefill(request, code):
    if request.method != "POST":
        return HttpResponseNotAllowed()

    