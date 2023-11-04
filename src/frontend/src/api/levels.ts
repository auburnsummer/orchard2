import { client } from "./client.ts";

import * as tg from "generic-type-guard";

type ColorToken = {
    len: number,
    color: string
}

export type VitalsLevelExport = {
    artist: string,
    artist_tokens: string[],
    song: string,
    song_ct: ColorToken[],
    seizure_warning: boolean,
    description: string,
    description_ct: ColorToken[],
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

const isColorToken: tg.TypeGuard<ColorToken> = tg.isLikeObject({
    len: tg.isNumber,
    color: tg.isString
});

const isVitalsExport: tg.TypeGuard<VitalsLevelExport> = tg.isLikeObject({
    artist: tg.isString,
    artist_tokens: tg.isArray(tg.isString),
    song: tg.isString,
    song_ct: tg.isArray(isColorToken),
    seizure_warning: tg.isBoolean,
    description: tg.isString,
    description_ct: tg.isArray(isColorToken),
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
export async function getLevelPrefill(publisherToken: string, userToken: string) {
    return client.post("level/prefill", {
        guard: isPrefillResult,
        headers: {
            authorization: `Bearer ${publisherToken},Bearer ${userToken}`
        }
    })
}