from django.shortcuts import render

# Create your views here.
def create_club(request):
    return render(request, "cafe/clubs/create_club.jinja")
