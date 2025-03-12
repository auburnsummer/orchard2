/**
 * Mapping of url path names (from server/cafe-backend/cafe/urls.py) to components to render.
 */

import { ClubSettingsCheckConnectDiscord } from "./views/ClubSettings/ClubSettingsCheckConnectDiscord/ClubSettingsCheckConnectDiscord";
import { ClubSettingsConnectDiscord } from "./views/ClubSettings/ClubSettingsConnectDiscord/ClubSettingsConnectDiscord";
import { ClubSettingsInfoView } from "./views/ClubSettings/ClubSettingsInfoView/ClubSettingsInfoView";
import { ClubSettingsMembersView } from "./views/ClubSettings/ClubSettingsMembersView/ClubSettingsMembersView";
import { HomeView } from "./views/HomeView";
import { LevelAddFromPrefill } from "./views/LevelAdd/LevelAddFromPrefill";
import { LevelAddTypeSelect } from "./views/LevelAdd/LevelAddTypeSelect";
import { ProfileClubsView } from "./views/Profile/ProfileClubsView/ProfileClubsView";
import { ProfileIndexView } from "./views/Profile/ProfileIndexView/ProfileIndexView";
import { ProfileSettingsView } from "./views/Profile/ProfileSettingsView/ProfileSettingsView";

export const appName = "cafe";

export const routeMap: { [key: string]: React.FunctionComponent<any> } = {
    "index": HomeView,
    "profile": ProfileIndexView,
    "profile_settings": ProfileSettingsView,
    "profile_clubs": ProfileClubsView,

    "club_connect_discord": ClubSettingsConnectDiscord,
    "club_settings_info": ClubSettingsInfoView,
    "club_settings_members": ClubSettingsMembersView,
    "club_settings_connected_discords": ClubSettingsCheckConnectDiscord,

    "level_portal": LevelAddTypeSelect,
    "level_from_prefill": LevelAddFromPrefill
}