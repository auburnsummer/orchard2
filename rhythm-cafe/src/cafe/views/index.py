from django.shortcuts import render
from loguru import logger

# Create your views here.
def index(request):
    return render(request, "cafe/index.jinja")
