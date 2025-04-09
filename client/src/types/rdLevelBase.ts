// corresponding to VitalsLevelBaseMutable
// I'd love to do some fancy type generating someday to get single source of truth
// but ehhhhhh
export type RDLevelBaseMutable = {
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
    single_player: number;
    two_player: number;
    tags: string[];
    has_classics: boolean;
    has_oneshots: boolean;
    has_squareshots: boolean;
    has_freezeshots: boolean;
    has_freetimes: boolean;
    has_holds: boolean;
    has_skipshots: boolean;
    has_window_dance: boolean;
};

export type RDLevelBase = RDLevelBaseMutable & {
    sha1: string
    rdlevel_sha1: string
    is_animated: boolean
    last_updated: string
};

export type RDLevel = RDLevelBase & {
    rdzip_url: string;
    image_url: string;
    icon_url?: string;
    thumb_url: string;
}