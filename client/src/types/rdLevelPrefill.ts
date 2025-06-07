import { RDLevelBase } from "./rdLevelBase"
import { Club } from "./club"
import { UserPublic } from "./user";

type RDLevelPrefillBase = {
    id: string;
    url: string;
    created_at: {
        _type: "Date";
        _args: string[];
    };
    version: number;
    prefill_type: string;
    user: UserPublic;
    club: Club;
}

type RDLevelPrefillNotReady = RDLevelPrefillBase & {
    ready: false;
    errors: string;
    data: Record<string, never>;
}

export type RDLevelPrefillReady = RDLevelPrefillBase & {
    ready: true;
    errors: "";
    data: RDLevelBase;
}

export type RDLevelPrefill = RDLevelPrefillNotReady | RDLevelPrefillReady;