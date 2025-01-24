from django.urls import path
from django.views.generic import TemplateView

from .views.index import index
from .views.accounts.profile.index import profile  
from .views.accounts.profile.profile_settings import settings as profile_settings
from .views.accounts.profile.profile_clubs import profile_clubs
from .views.clubs.create_club import create_club

from .views.clubs.settings.info import info

from .views.login import login

urlpatterns = [
    path("", index, name="index"),

    path("accounts/login/", login, name="login"),
    path("accounts/profile/", profile, name="profile"),
    path("accounts/profile/settings/", profile_settings, name="profile_settings"),
    path("accounts/profile/groups/", profile_clubs, name="profile_clubs"),

    path("groups/create/", create_club, name="create_club"),

    path("groups/<club_id>/settings/", info, name="club_settings_info"),
]