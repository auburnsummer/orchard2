from django.shortcuts import render

# Create your views here.
def notfound(request):
    return render(request, "cafe/errors/notfound.jinja")
