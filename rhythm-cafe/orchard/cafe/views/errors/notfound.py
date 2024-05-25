from django.shortcuts import render

# Create your views here.
def notfound(request, exception):
    return render(request, "cafe/errors/notfound.jinja", status=404)
