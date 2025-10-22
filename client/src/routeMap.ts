/**
 * Mapping of url path names (from server/cafe-backend/cafe/urls.py) to components to render.
 */

import { ClubSettingsCheckConnectDiscord } from "./views/ClubSettings/ClubSettingsCheckConnectDiscord/ClubSettingsCheckConnectDiscord";
import { ClubSettingsConnectDiscord } from "./views/ClubSettings/ClubSettingsConnectDiscord/ClubSettingsConnectDiscord";
import { ClubSettingsInfoView } from "./views/ClubSettings/ClubSettingsInfoView";
import { ClubSettingsMembersView } from "./views/ClubSettings/ClubSettingsMembersView/ClubSettingsMembersView";
import { HomeView } from "./views/HomeView";
import { LevelEdit } from "./views/Level/LevelEdit/LevelEdit";
import { LevelView } from "./views/Level/LevelView/LevelView";
import { LevelSearch } from "./views/Level/LevelSearch/LevelSearch";
import { LevelAddFromPrefill } from "./views/LevelAdd/LevelAddFromPrefill/LevelAddFromPrefill";
import { LevelAddTypeSelect } from "./views/LevelAdd/LevelAddTypeSelect";
import { ProfileClubsView } from "./views/Profile/ProfileClubsView";
import { ProfileIndexView } from "./views/Profile/ProfileIndexView";
import { ProfileSettingsView } from "./views/Profile/ProfileSettingsView";
import { ClubSettingsRedeemInvite } from "./views/ClubSettings/ClubSettingsRedeemInvite/ClubSettingsRedeemInvite";

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

  "cafe:redeem_invite": ClubSettingsRedeemInvite,

  "cafe:level_portal": LevelAddTypeSelect,
  "cafe:level_from_prefill": LevelAddFromPrefill,
  "cafe:level_search": LevelSearch,
  "cafe:level_view": LevelView,
  "cafe:level_edit": LevelEdit,
};
