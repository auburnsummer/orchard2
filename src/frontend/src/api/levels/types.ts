import * as tg from "generic-type-guard";

/**
 * corresponds to VitalsLevelBaseMutable in libs/vitals/msgspec_schema.py
 */
type VitalsLevelBaseMutable = {
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
}

const vitalsLevelBaseMutableGuards = {
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
    has_window_dance: tg.isBoolean
}

export const isVitalsLevelBaseMutable: tg.TypeGuard<VitalsLevelBaseMutable> = tg.isLikeObject(vitalsLevelBaseMutableGuards)

/**
 * Corresponds to VitalsLevelBase in libs/vitals/msgspec_schema.py
 */
type VitalsLevelBase = VitalsLevelBaseMutable & {
    sha1: string;
    rdlevel_sha1: string;
    is_animated: boolean;
}

const vitalsLevelBaseGuards = {
    ...vitalsLevelBaseMutableGuards,
    sha1: tg.isString,
    rdlevel_sha1: tg.isString,
    image: tg.isString,
    is_animated: tg.isBoolean,

}

export const isVitalsLevelBase: tg.TypeGuard<VitalsLevelBase> = tg.isLikeObject(vitalsLevelBaseGuards);

/**
 * Corresponds to RDPrefillResult in v1/models/rd_levels.py
 */
type RDPrefillResult = VitalsLevelBase & {
    image: string;
    thumb: string;
    url: string;
    icon?: string;
}

const rdPrefillResultGuards = {
    ...vitalsLevelBaseGuards,
    image: tg.isString,
    thumb: tg.isString,
    url: tg.isString,
    icon: tg.isOptional(tg.isString)
}

export const isRDPrefillResult: tg.TypeGuard<RDPrefillResult> = tg.isLikeObject(rdPrefillResultGuards);

/**
 * Corresponds to RDPrefillResultWithToken in v1/models/rd_levels.py
 */
type RDPrefillResultWithToken = {
    result: RDPrefillResult,
    signed_token: string;
}

export const isRDPrefillResultWithToken: tg.TypeGuard<RDPrefillResultWithToken> = tg.isLikeObject({
    result: isRDPrefillResult,
    signed_token: tg.isString
})