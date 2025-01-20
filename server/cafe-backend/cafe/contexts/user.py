from django.urls import reverse

from allauth.socialaccount.models import SocialAccount
from cafe.views.types import HttpRequest

def user(request: HttpRequest):
    if request.user.is_authenticated:
        return request.user.to_dict()
    else:
        return {
            "authenticated": False
        }