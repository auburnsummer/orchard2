/**
 * Mapping of url path names (from server/cafe-backend/cafe/urls.py) to components to render.
 */

import { HomeView } from "./views/HomeView";
import { LevelEdit } from "./views/Level/LevelEdit";
import { LevelView } from "./views/Level/LevelView/LevelView";
import { LevelSearch } from "./views/Level/LevelSearch/LevelSearch";
import { LevelAddFromPrefill } from "./views/LevelAdd/LevelAddFromPrefill/LevelAddFromPrefill";
import { LevelAddTypeSelect } from "./views/LevelAdd/LevelAddTypeSelect";
import { ProfileClubsView } from "./views/Profile/ProfileClubsView";
import { ProfileIndexView } from "./views/Profile/ProfileIndexView";
import { ProfileSettingsView } from "./views/Profile/ProfileSettingsView";
import { ClubSettingsRedeemInvite } from "./views/ClubSettings/ClubSettingsRedeemInvite";
import { ProfileApiKeyView } from "./views/Profile/ProfileApiKeyView";
import React from "react";
import { ProfileDeleteAccount } from "./views/Profile/ProfileDeleteAccount";

// most people won't go to PR, so lazy load it
const PeerReviewMainView = React.lazy(() => import("./views/PeerReview/PeerReviewMainView").then(m => ({ default: m.PeerReviewMainView })));
const PeerReviewConfiguration = React.lazy(() => import("./views/PeerReview/PeerReviewConfiguration").then(m => ({ default: m.PeerReviewConfiguration })));
const PeerReviewLevelView = React.lazy(() => import("./views/PeerReview/PeerReviewLevelView").then(m => ({ default: m.PeerReviewLevelView })));
const PeerReviewMakeEncryptedWebhook = React.lazy(() => import("./views/PeerReview/PeerReviewMakeEncryptedWebhook").then(m => ({ default: m.PeerReviewMakeEncryptedWebhook })));

const DailyBlendMainView = React.lazy(() => import("./views/DailyBlend/DailyBlendMainView").then(m => ({ default: m.DailyBlendMainView })));
const DailyBlendConfiguration = React.lazy(() => import("./views/DailyBlend/DailyBlendConfiguration").then(m => ({ default: m.DailyBlendConfiguration })));
const DailyBlendRandomPool = React.lazy(() => import("./views/DailyBlend/DailyBlendRandomPool").then(m => ({ default: m.DailyBlendRandomPool })));
const DailyBlendSchedule = React.lazy(() => import("./views/DailyBlend/DailyBlendSchedule").then(m => ({ default: m.DailyBlendSchedule })));
const DailyBlendBlendNow = React.lazy(() => import("./views/DailyBlend/DailyBlendBlendNow").then(m => ({ default: m.DailyBlendBlendNow })));

const ClubSettingsConnectDiscord = React.lazy(() => import("./views/ClubSettings/ClubSettingsConnectDiscord").then(m => ({ default: m.ClubSettingsConnectDiscord })));
const ClubSettingsInfoView = React.lazy(() => import("./views/ClubSettings/ClubSettingsInfoView").then(m => ({ default: m.ClubSettingsInfoView })));
const ClubSettingsMembersView = React.lazy(() => import("./views/ClubSettings/ClubSettingsMembersView/ClubSettingsMembersView").then(m => ({ default: m.ClubSettingsMembersView })));
const ClubSettingsCheckConnectDiscord = React.lazy(() => import("./views/ClubSettings/ClubSettingsCheckConnectDiscord").then(m => ({ default: m.ClubSettingsCheckConnectDiscord })));
const ClubSettingsDeleteView = React.lazy(() => import("./views/ClubSettings/ClubSettingsDelete").then(m => ({ default: m.ClubSettingsDeleteView })));

export const appName = "cafe";

export const routeMap: { [key: string]: React.FunctionComponent<any> } = {
  "cafe:index": HomeView,
  "cafe:profile": ProfileIndexView,
  "cafe:profile_settings": ProfileSettingsView,
  "cafe:profile_clubs": ProfileClubsView,
  "cafe:profile_api_key": ProfileApiKeyView,
  "cafe:profile_delete_account": ProfileDeleteAccount,

  "cafe:club_connect_discord": ClubSettingsConnectDiscord,
  "cafe:club_settings_info": ClubSettingsInfoView,
  "cafe:club_settings_members": ClubSettingsMembersView,
  "cafe:club_settings_connected_discords": ClubSettingsCheckConnectDiscord,
  "cafe:club_delete": ClubSettingsDeleteView,

  "cafe:redeem_invite": ClubSettingsRedeemInvite,

  "cafe:level_portal": LevelAddTypeSelect,
  "cafe:level_from_prefill": LevelAddFromPrefill,
  "cafe:level_search": LevelSearch,
  "cafe:level_view": LevelView,
  "cafe:level_edit": LevelEdit,

  "cafe:peer_review_main": PeerReviewMainView,
  "cafe:peer_review_config": PeerReviewConfiguration,
  "cafe:peer_review_level": PeerReviewLevelView,
  "cafe:peer_review_make_encrypted_webhook": PeerReviewMakeEncryptedWebhook,

  "cafe:blend_main": DailyBlendMainView,
  "cafe:blend_config": DailyBlendConfiguration,
  "cafe:blend_pool": DailyBlendRandomPool,
  "cafe:blend_schedule": DailyBlendSchedule,
  "cafe:blend_now": DailyBlendBlendNow,
};
