from django.urls import path

from .views.index import index
from .views.accounts.profile.index import profile  
from .views.accounts.profile.profile_settings import settings as profile_settings

urlpatterns = [
    path("", index, name="index"),
    path("accounts/profile/", profile, name="profile"),
    path("accounts/profile/settings/", profile_settings, name="profile_settings"),
]