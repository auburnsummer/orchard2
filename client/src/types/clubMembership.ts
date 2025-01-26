import { AuthenticatedUser } from "@cafe/hooks/useUser";
import { Club } from "./club";

export type ClubMembershipRole = 'admin' | 'owner';

export type ClubMembership = {
    user: AuthenticatedUser;
    club: Club;
    role: ClubMembershipRole;
}