import { User } from "./auth.ts";
import { client } from "./client.ts";

import * as tg from "generic-type-guard";
import { Publisher } from "./publisher.ts";

/**
 * corresponds to VitalsLevelBase in libs/vitals/pydantic_model.py
 * excludes song_ct and description_ct as we don't store those and I'm
 * probably going to get rid of those in the future anyway.
 */
type VitalsLevelBase = {
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
    last_updated: string;
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
}

const vitalsLevelBaseGuards = {
    artist: tg.isString,
    artist_tokens: tg.isArray(tg.isString),
    song: tg.isString,
    seizure_warning: tg.isBoolean,
    description: tg.isString,
    hue: tg.isNumber,
    authors: tg.isArray(tg.isString),
    authors_raw: tg.isString,
    max_bpm: tg.isNumber,
    min_bpm: tg.isNumber,
    difficulty: tg.isNumber,
    single_player: tg.isBoolean,
    two_player: tg.isBoolean,
    last_updated: tg.isString,
    tags: tg.isArray(tg.isString),
    has_classics: tg.isBoolean,
    has_oneshots: tg.isBoolean,
    has_squareshots: tg.isBoolean,
    has_freezeshots: tg.isBoolean,
    has_freetimes: tg.isBoolean,
    has_holds: tg.isBoolean,
    has_skipshots: tg.isBoolean,
    has_window_dance: tg.isBoolean,
    sha1: tg.isString,
    rdlevel_sha1: tg.isString,
    image: tg.isString,
    is_animated: tg.isBoolean,
}

// const isVitalsLevelBase : tg.TypeGuard<VitalsLevelBase> = tg.isLikeObject(vitalsLevelBaseGuards);

/**
 * Corresponds to RDPrefillResult in models/rd_levels.py
 */
export type RDPrefillResult = VitalsLevelBase & {
    image: string;
    thumb: string;
    url: string;
    icon?: string;
};

const isRDPrefillResult: tg.TypeGuard<RDPrefillResult> = tg.isLikeObject({
    ...vitalsLevelBaseGuards,
    image: tg.isString,
    thumb: tg.isString,
    url: tg.isString,
    icon: tg.isOptional(tg.isString)
});

/**
 * The main level type. e.g. the return type for GET /rdlevel/{id}
 */
export type RDLevel = RDPrefillResult & {
    song_alt: string;
    uploader: User;
    publisher: Publisher;
    uploaded: string;  // datetime
    approval: number;  // int
}

/**
 * The response type of the POST /rdlevel/prefill endpoint.
 */
export type RDPrefillResultWithToken = {
    result: RDPrefillResult;
    signed_token: string;
}

const isRDPrefillResultWithToken : tg.TypeGuard<RDPrefillResultWithToken> = tg.isLikeObject({
    result: isRDPrefillResult,
    signed_token: tg.isString
});


// fields not used in the add level endpoint.
type PropsNotUsedInAddLevel = 
    "sha1" |
    "rdlevel_sha1" |
    "is_animated"

// the main field required for the add level endpoint. 
export type RDPrefillResultTruncated = Omit<VitalsLevelBase, PropsNotUsedInAddLevel> & {
    song_alt: string;
}

type AddRDLevelPayload = {
    level: RDPrefillResultTruncated
}

// the url for the prefill is encoded in the token and cannot be changed by the user.
export async function getRDLevelPrefill(publisherToken: string) {
    return client.post("rdlevel/prefill", {
        guard: isRDPrefillResultWithToken,
        headers: {
            authorization: `Bearer ${publisherToken}`
        }
    })
}


// export async function addRDLevel(prefillSignedToken: string, payload: AddRDLevelPayload) {
//     return client.post("rdlevel", {
//         guard
//     })
// }