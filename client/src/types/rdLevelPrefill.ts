import { RDLevelBase } from "./rdLevelBase";
import { Club } from "./club";
import { UserPublic } from "./user";

type RDLevelPrefillBase = {
  id: string;
  url: string;
  created_at: string;
  version: number;
  prefill_type: "update" | "new";
  go_to_prepost: boolean;
  user: UserPublic;
  club: Club;
};

type RDLevelPrefillNotReady = RDLevelPrefillBase & {
  ready: false;
  errors: string;
  data: Record<string, never>;
};

type RDLevelPrefillReadyBase = RDLevelPrefillBase & {
  ready: true;
  errors: "";
  data: RDLevelBase;
}

export type RDLevelPrefillReady = RDLevelPrefillReadyBase & {
  prefill_type: "new";
  go_to_prepost: true;
};

export type RDLevelPrefillReadyNoPrepost = RDLevelPrefillReadyBase & {
  prefill_type: "new";
  go_to_prepost: false;
  level_id: string;
}

export type RDLevelPrefillUpdateReady = RDLevelPrefillBase & {
  ready: true;
  errors: "";
  data: RDLevelBase;
} & {
  prefill_type: "update";
};

export type RDLevelPrefill =
  | RDLevelPrefillNotReady
  | RDLevelPrefillReady
  | RDLevelPrefillUpdateReady
  | RDLevelPrefillReadyNoPrepost;
