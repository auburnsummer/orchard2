from django.shortcuts import render

def login(request):
    return render(request, "cafe/accounts/login.jinja")