/**
 * Mapping of url path names (from server/cafe-backend/cafe/urls.py) to components to render.
 */

import { ClubSettingsInfoView } from "./views/ClubSettings/ClubSettingsInfoView/ClubSettingsInfoView";
import { ClubSettingsMembersView } from "./views/ClubSettings/ClubSettingsMembersView/ClubSettingsMembersView";
import { CreateClubView } from "./views/CreateClubView/CreateClubView";
import { HomeView } from "./views/HomeView";
import { ProfileClubsView } from "./views/Profile/ProfileClubsView/ProfileClubsView";
import { ProfileIndexView } from "./views/Profile/ProfileIndexView/ProfileIndexView";
import { ProfileSettingsView } from "./views/Profile/ProfileSettingsView/ProfileSettingsView";

export const routeMap: { [key: string]: React.FunctionComponent<any> } = {
    "index": HomeView,
    "profile": ProfileIndexView,
    "profile_settings": ProfileSettingsView,
    "profile_clubs": ProfileClubsView,
    
    "create_club": CreateClubView,
    "club_settings_info": ClubSettingsInfoView,
    "club_settings_members": ClubSettingsMembersView
}