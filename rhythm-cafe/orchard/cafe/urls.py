from django.urls import path

from . import views
from django.contrib.auth import views as auth_views

app_name = "cafe"
urlpatterns = [
    path("discord_interactions/", views.discord_bot.entry, name="discord_interactions"),

    path("accounts/login/", views.accounts.login, name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("accounts/profile/", views.profile.profile, name="profile"),
    path("accounts/profile/groups/", views.profile.clubs, name="clubs"),
    path("accounts/profile/settings/", views.profile.settings, name="settings"),
    path("accounts/profile/connections/", views.profile.connections, name="connections"),

    path("groups/create/", views.clubs.create_club, name="create_club"),

    path("groups/redeem_invite/<code>/", views.clubs.redeem_invite, name="redeem_invite"),
    path("groups/connect_discord/<code>/", views.clubs.connect_discord_form, name="connect_club_discord"),
    
    path("groups/<club_id>/settings/", views.club_settings.info, name="club_settings_info"),
    path("groups/<club_id>/settings/invite/", views.club_settings.create_invite, name="club_settings_membership_invite"),
    path("groups/<club_id>/settings/connections/", views.club_settings.connections, name="club_settings_connections"),
    path("groups/<club_id>/settings/members/", views.club_settings.members, name="club_settings_members"),
    path("groups/<club_id>/settings/members/<user_id>/", views.club_settings.alter_membership, name="club_settings_membership"),
    path("groups/<club_id>/settings/members/<user_id>/delete/", views.club_settings.delete_membership, name="club_settings_membership_delete"),

    path("levels/add/<code>/", views.levels.add, name="level_add"),
    path("levels/add/<code>/prefill/", views.index, name="level_prefill"),

    path("meta/all_styles.css/", views.meta.combined_css, name="combined_css"),

    path("", views.index, name="index")
]