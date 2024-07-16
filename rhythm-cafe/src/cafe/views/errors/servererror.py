from django.shortcuts import render

import sys

from cafe.libs.errors import OrchardException

# Create your views here.
def servererror(request):
    type_, value, _ = sys.exc_info()
    if not issubclass(type_, OrchardException):
        value = "An unknown error occurred."

    return render(request, "cafe/errors/servererror.jinja", { "error_message": value }, status=500)
