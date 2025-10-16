import { RDLevelBase } from "./rdLevelBase";
import { Club } from "./club";
import { UserPublic } from "./user";

type RDLevelPrefillBase = {
  id: string;
  url: string;
  created_at: {
    _type: "Date";
    _args: string[];
  };
  version: number;
  prefill_type: "update" | "new";
  user: UserPublic;
  club: Club;
};

type RDLevelPrefillNotReady = RDLevelPrefillBase & {
  ready: false;
  errors: string;
  data: Record<string, never>;
};

export type RDLevelPrefillReady = RDLevelPrefillBase & {
  ready: true;
  errors: "";
  data: RDLevelBase;
} & {
  prefill_type: "new";
};

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
  | RDLevelPrefillUpdateReady;
