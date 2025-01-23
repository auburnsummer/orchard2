/**
 * Mapping of url path names (from server/cafe-backend/cafe/urls.py) to components to render.
 */

import { CreateClubView } from "./views/CreateClubView/CreateClubView";
import { HomeView } from "./views/HomeView";
import { ProfileClubsView } from "./views/Profile/ProfileClubsView/ProfileClubsView";
import { ProfileIndexView } from "./views/Profile/ProfileIndexView/ProfileIndexView";
import { ProfileSettingsView } from "./views/Profile/ProfileSettingsView/ProfileSettingsView";

export const routeMap: { [key: string]: React.ComponentType<any> } = {
    "index": HomeView,
    "profile": ProfileIndexView,
    "profile_settings": ProfileSettingsView,
    "profile_clubs": ProfileClubsView,
    
    "create_club": CreateClubView
}