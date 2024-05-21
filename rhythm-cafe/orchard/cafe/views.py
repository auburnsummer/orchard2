from django.shortcuts import render
from django.http import HttpResponse

from cafe.templates.environment import env

# Create your views here.
def index(request):
    template = env.get_template("index.jinja")
    return HttpResponse(template.render())
