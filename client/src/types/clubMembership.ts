import { Club } from "./club";
import { UserPublic } from "./user";

export type ClubMembershipRole = 'admin' | 'owner';

export type ClubMembership = {
    user: UserPublic;
    club: Club;
    role: ClubMembershipRole;
}