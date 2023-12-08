import * as tg from "generic-type-guard";
import { User, isUser } from "../auth";
import { Publisher, isPublisher } from "..";

/**
 * corresponds to VitalsLevelBaseMutable in libs/vitals/msgspec_schema.py
 */
export type VitalsLevelBaseMutable = {
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
export type RDPrefillResult = VitalsLevelBase & {
    image: string;
    thumb: string;
    url: string;
    icon: string | null;
}

const rdPrefillResultGuards = {
    ...vitalsLevelBaseGuards,
    image: tg.isString,
    thumb: tg.isString,
    url: tg.isString,
    icon: tg.isNullable(tg.isString)
}

export const isRDPrefillResult: tg.TypeGuard<RDPrefillResult> = tg.isLikeObject(rdPrefillResultGuards);

/**
 * Corresponds to RDPrefillResultWithToken in v1/models/rd_levels.py
 */
export type RDPrefillResultWithToken = {
    result: RDPrefillResult,
    signed_token: string;
}

export const isRDPrefillResultWithToken: tg.TypeGuard<RDPrefillResultWithToken> = tg.isLikeObject({
    result: isRDPrefillResult,
    signed_token: tg.isString
})


/**
 * Corresponds to AddRDLevelPayload in v1/routes/rd_levels.py
 */
export type AddRDLevelPayload = VitalsLevelBaseMutable & {
    song_alt: string;
}

/**
 * Corresponds to RDLevel in v1/models/rd_levels.py
 */
export type RDLevel = RDPrefillResult & AddRDLevelPayload & {
    uploader: User
    publisher: Publisher

    uploaded: string // datetime
    approval: number
}

export const isRDLevel: tg.TypeGuard<RDLevel> = tg.isLikeObject({
    ...rdPrefillResultGuards,
    id: tg.isString,
    song_alt: tg.isString,
    uploader: isUser,
    publisher: isPublisher,
    uploaded: tg.isString,
    approval: tg.isNumber
})

/**
 * Corresponds to AddRDLevelResponse in v1/routes/rd_levels.py
 */
export type AddRDLevelResponse = {
    level: RDLevel
}

export const isAddRDLevelResponse: tg.TypeGuard<AddRDLevelResponse> = tg.isLikeObject({
    level: isRDLevel
})

/**
 * Corresponds to RDSearchParams in v1/models/rd_levels.py
 */
export type RDSearchParams = {
    q?: string;
    tags?: string[];
    artists?: string[];
    authors?: string[];
    min_bpm?: number;
    max_bpm?: number;
    difficulty?: string[];
    single_player?: boolean;
    two_player?: boolean;
    has_classics?: boolean;
    has_oneshots?: boolean;
    has_squareshots?: boolean;
    has_freezeshots?: boolean;
    has_freetimes?: boolean;
    has_holds?: boolean;
    has_skipshots?: boolean;
    has_window_dance?: boolean;

    uploader?: string;
    publisher?: string;

    min_approval?: number;
    max_approval?: number;

    offset?: number;
    limit?: number;
}

/**
 * Corresponds to StrFacetValue in v1/models/rd_levels.py
 */
export type StrFacetValue = {
    value: string;
    count: number;
}

export const isStrFacetValue: tg.TypeGuard<StrFacetValue> = tg.isLikeObject({
    value: tg.isString,
    count: tg.isNumber
});

/**
 * Corresponds to IntFacetValue in v1/models/rd_levels.py
 */
export type IntFacetValue = {
    value: number;
    count: number;
}

export const isIntFacetValue: tg.TypeGuard<IntFacetValue> = tg.isLikeObject({
    value: tg.isNumber,
    count: tg.isNumber
})

/**
 * Corresponds to RDQueryResult in v1/models/rd_levels.py
 */
export type RDQueryResult = {
    levels: RDLevel[];
    tags: StrFacetValue[];
    artists: StrFacetValue[];
    authors: StrFacetValue[];
    difficulties: IntFacetValue[];
} 

export const isRDQueryResult: tg.TypeGuard<RDQueryResult> = tg.isLikeObject({
    levels: tg.isArray(isRDLevel),
    tags: tg.isArray(isStrFacetValue),
    artists: tg.isArray(isStrFacetValue),
    authors: tg.isArray(isStrFacetValue),
    difficulties: tg.isArray(isIntFacetValue)
});