import { client } from "./client.ts";

import * as tg from "generic-type-guard";


export type VitalsLevelExport = {
    artist_tokens: string[],
    song: string,
    seizure_warning: boolean,
    description: string,
    hue: number,
    authors: string[],
    authors_raw: string,
    max_bpm: number,
    min_bpm: number,
    difficulty: number,
    single_player: boolean,
    two_player: boolean,
    last_updated: string,
    tags: string[],
    has_classics: boolean,
    has_oneshots: boolean,
    has_squareshots: boolean,
    has_freezeshots: boolean,
    has_freetimes: boolean,
    has_holds: boolean,
    has_skipshots: boolean,
    has_window_dance: boolean,
    sha1: string,
    rdlevel_sha1: string
    image: string,
    is_animated: boolean,
    thumb: string,
    url: string,
    icon?: string
};

export type PrefillResult = {
    result: VitalsLevelExport,
    signed_token: string
}

const isVitalsExport: tg.TypeGuard<VitalsLevelExport> = tg.isLikeObject({
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
    thumb: tg.isString,
    url: tg.isString,
    icon: tg.isOptional(tg.isString),
});

const isPrefillResult : tg.TypeGuard<PrefillResult> = tg.isLikeObject({
    result: isVitalsExport,
    signed_token: tg.isString
});

// the url for the prefill is encoded in the token and cannot be changed by the user.
export async function getRDLevelPrefill(publisherToken: string) {
    return client.post("rdlevel/prefill", {
        guard: isPrefillResult,
        headers: {
            authorization: `Bearer ${publisherToken}`
        }
    })
}

export async function addRDLevel() {

}