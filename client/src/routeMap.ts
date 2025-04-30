/**
 * Mapping of url path names (from server/cafe-backend/cafe/urls.py) to components to render.
 */

import { ClubSettingsCheckConnectDiscord } from "./views/ClubSettings/ClubSettingsCheckConnectDiscord/ClubSettingsCheckConnectDiscord";
import { ClubSettingsConnectDiscord } from "./views/ClubSettings/ClubSettingsConnectDiscord/ClubSettingsConnectDiscord";
import { ClubSettingsInfoView } from "./views/ClubSettings/ClubSettingsInfoView/ClubSettingsInfoView";
import { ClubSettingsMembersView } from "./views/ClubSettings/ClubSettingsMembersView/ClubSettingsMembersView";
import { HomeView } from "./views/HomeView";
import { LevelView } from "./views/Level/LevelView";
import { LevelAddFromPrefill } from "./views/LevelAdd/LevelAddFromPrefill/LevelAddFromPrefill";
import { LevelAddTypeSelect } from "./views/LevelAdd/LevelAddTypeSelect";
import { ProfileClubsView } from "./views/Profile/ProfileClubsView/ProfileClubsView";
import { ProfileIndexView } from "./views/Profile/ProfileIndexView/ProfileIndexView";
import { ProfileSettingsView } from "./views/Profile/ProfileSettingsView/ProfileSettingsView";

export const appName = "cafe";

export const routeMap: { [key: string]: React.FunctionComponent<any> } = {
    "cafe:index": HomeView,
    "cafe:profile": ProfileIndexView,
    "cafe:profile_settings": ProfileSettingsView,
    "cafe:profile_clubs": ProfileClubsView,

    "cafe:club_connect_discord": ClubSettingsConnectDiscord,
    "cafe:club_settings_info": ClubSettingsInfoView,
    "cafe:club_settings_members": ClubSettingsMembersView,
    "cafe:club_settings_connected_discords": ClubSettingsCheckConnectDiscord,

    "cafe:level_portal": LevelAddTypeSelect,
    "cafe:level_from_prefill": LevelAddFromPrefill,
    "cafe:level_view": LevelView
}