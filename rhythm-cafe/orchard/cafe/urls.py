from django.urls import path

from . import views

urlpatterns = [
    path("accounts/profile/", views.profile.profile, name="profile"),
    path("", views.index, name="index")
]