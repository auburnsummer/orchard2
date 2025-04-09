import { AuthenticatedUser } from "@cafe/hooks/useUser"
import { RDLevel } from "./rdLevelBase"
import { Club } from "./club"

export type RDLevelPrefill = {
    id: string;
    url: string;
    created_at: {
        _type: "Date";
        _args: string[];
    };
    version: number;
    prefill_type: string;
    ready: boolean;
    data: RDLevel;
    user: AuthenticatedUser;
    club: Club;
    errors: string;
}