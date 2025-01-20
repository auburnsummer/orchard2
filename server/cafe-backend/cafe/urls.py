from django.urls import path
from django.views.generic import TemplateView

from .views.index import index
from .views.accounts.profile.index import profile  
from .views.accounts.profile.profile_settings import settings as profile_settings
from .views.clubs.create_club import create_club


urlpatterns = [
    path("", index, name="index"),
    
    path("accounts/login/", TemplateView.as_view(template_name="cafe/login.html")),
    path("accounts/profile/", profile, name="profile"),
    path("accounts/profile/settings/", profile_settings, name="profile_settings"),

    path("groups/create/", create_club, name="create_club")
]