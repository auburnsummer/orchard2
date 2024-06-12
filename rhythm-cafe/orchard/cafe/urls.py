from django.urls import path

from . import views

app_name = "cafe"
urlpatterns = [
    path("discord_interactions", views.discord_bot.entry, name="discord_interactions"),

    path("accounts/profile/", views.profile.profile, name="profile"),
    path("accounts/profile/groups/", views.profile.clubs, name="clubs"),
    path("accounts/profile/settings/", views.profile.settings, name="settings"),
    path("accounts/profile/connections/", views.profile.connections, name="connections"),

    path("groups/create/", views.clubs.create_club, name="create_club"),

    path("groups/<group_id>/settings/", views.club_settings.members, name="club_settings_members"),

    path("", views.index, name="index")
]