from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "cafe/index.jinja", { "user": request.user })
