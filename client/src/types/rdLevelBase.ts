import { AuthenticatedUser } from "@cafe/hooks/useUser";
import { Club } from "./club";

// output of the prefill job
export type RDLevelBase = {
    artist: string;
    artist_tokens: string[];
    song: string;
    seizure_warning: boolean;
    description: string;
    hue: number;
    authors: string[];
    authors_raw: string;
    max_bpm: number;
    min_bpm: number;
    difficulty: number;
    single_player: boolean;
    two_player: boolean;
    tags: string[];
    has_classics: boolean;
    has_oneshots: boolean;
    has_squareshots: boolean;
    has_freezeshots: boolean;
    has_freetimes: boolean;
    has_holds: boolean;
    has_skipshots: boolean;
    has_window_dance: boolean;

    sha1: string;
    rdlevel_sha1: string;
    is_animated: boolean;
    last_updated: string;
    rdzip_url: string;
    image_url: string;
    icon_url?: string;
    thumb_url: string;
};

// some additional fields
export type RDLevel = RDLevelBase & {
    song_alt: string;
    submitter: AuthenticatedUser;
    club: Club;
    approval: number;
}