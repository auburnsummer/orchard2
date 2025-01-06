from django.urls import path

from .views.index import index
from .views.accounts.profile.index import profile  

urlpatterns = [
    path("", index, name="index"),
    path("accounts/profile/", profile, name="profile"),
]