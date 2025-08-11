from django.urls import path
from django.views.generic import TemplateView

from .views.index import index
from .views.accounts.profile.index import profile  
from .views.accounts.profile.profile_settings import settings as profile_settings
from .views.accounts.profile.profile_clubs import profile_clubs
from .views.clubs.create_club import create_club
from .views.rdlevels.search_levels import search_levels

from .views.clubs.settings.info import info
from .views.clubs.settings.members import members
from .views.clubs.settings.membership import alter_membership, delete_membership
from .views.clubs.settings.create_invite import create_invite
from .views.clubs.settings.connected_discords import connected_discords
from .views.clubs.redeem_invite import redeem_invite
from .views.clubs.connect_discord import connect_discord

from .views.login import login

from .views.discord_bot.entry import entry
from .views.rdlevels.delete_rdlevel import delete_rdlevel
from .views.rdlevels.edit_rdlevel import edit_rdlevel

from .views.rdlevels.prefill.prefill_stage_one import prefill_stage_one
from .views.rdlevels.prefill.prefill_stage_two import prefill_stage_two
from .views.rdlevels.view_rdlevel import view_rdlevel

def trigger_error(request):
    division_by_zero = 1 / 0

app_name = "cafe"
urlpatterns = [
    path("", index, name="index"),

    path("discord_interactions/", entry, name="discord_interactions"),
    path("discord_interactions2/", entry, name="discord_interactions2"),

    path("accounts/login/", login, name="login"),
    path("accounts/profile/", profile, name="profile"),
    path("accounts/profile/settings/", profile_settings, name="profile_settings"),
    path("accounts/profile/groups/", profile_clubs, name="profile_clubs"),

    path("groups/create/", create_club, name="create_club"),

    path("groups/redeem_invite/<code>/", redeem_invite, name="redeem_invite"),
    path("groups/connect_discord/<code>/", connect_discord, name="club_connect_discord"),

    path("groups/<club_id>/settings/", info, name="club_settings_info"),
    path("groups/<club_id>/settings/members/", members, name="club_settings_members"),
    path("groups/<club_id>/settings/members/invite/", create_invite, name="club_settings_membership_invite"),
    path("groups/<club_id>/settings/members/<user_id>/edit/", alter_membership, name="club_settings_alter_membership"),
    path("groups/<club_id>/settings/members/<user_id>/delete/", delete_membership, name="club_settings_delete_membership"),
    path("groups/<club_id>/settings/connections/discord/", connected_discords, name="club_settings_connected_discords"),

    path("levels/add/<code>/", prefill_stage_one, name="level_portal"),
    path("levels/from_prefill/<prefill_id>/", prefill_stage_two, name="level_from_prefill"),
    path("levels/<level_id>", view_rdlevel, name="level_view"),
    path("levels/<level_id>/edit/", edit_rdlevel, name="level_edit"),
    path("levels/<level_id>/delete/", delete_rdlevel, name="level_delete"),
    path("levels/", search_levels, name="level_search")
]