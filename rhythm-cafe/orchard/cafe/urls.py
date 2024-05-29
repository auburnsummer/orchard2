from django.urls import path

from . import views

app_name = "cafe"
urlpatterns = [
    path("discord_interactions", views.discord_bot.entry, name="discord_interactions"),
    path("accounts/profile/settings/", views.profile.settings, name="settings"),
    path("accounts/profile/connections/", views.profile.connections, name="connections"),
    path("accounts/profile/", views.profile.profile, name="profile"),
    path("", views.index, name="index")
]