import * as tg from "generic-type-guard";

// todo: can we figure out a nice way to avoid duplicating the types between
// python and ts

export type ColorToken = {
    len: number
    color: string
}

export const IsColorToken: tg.TypeGuard<ColorToken> = tg.isLikeObject({
    len: tg.isNumber,
    color: tg.isString
})

export type LevelBase = {
    artist: string
    artist_tokens: string[]
    song: string
    song_ct: ColorToken[]
    seizure_warning: boolean
    description: string
    description_ct: ColorToken[]
    hue: number
    authors: string[]
    authors_raw: string
    max_bpm: number
    min_bpm: number
    difficulty: number
    single_player: boolean
    two_player: boolean
    last_updated: string
    tags: string[]
    has_classics: boolean
    has_oneshots: boolean
    has_squareshots: boolean
    has_freezeshots: boolean
    has_freetimes: boolean
    has_holds: boolean
    has_skipshots: boolean
    has_window_dance: boolean
    sha1: string
    rdlevel_sha1: string
}

export const isLevelBase: tg.TypeGuard<LevelBase> = tg.isLikeObject({
    artist: tg.isString,
    artist_tokens: tg.isArray(tg.isString),
    song: tg.isString,
    song_ct: tg.isArray(IsColorToken),
    seizure_warning: tg.isBoolean,
    description: tg.isString,
    description_ct: tg.isArray(IsColorToken),
    hue: tg.isFloat,
    authors: tg.isArray(tg.isString),
    authors_raw: tg.isString,
    max_bpm: tg.isNumber,
    min_bpm: tg.isNumber,
    difficulty: tg.isNumber,
    single_player: tg.isBoolean,
    two_player: tg.isBoolean,
    last_updated: tg.isString,
    has_classics: tg.isBoolean,
    has_freetimes: tg.isBoolean,
    has_freezeshots: tg.isBoolean,
    has_holds: tg.isBoolean,
    has_oneshots: tg.isBoolean,
    has_skipshots: tg.isBoolean,
    has_squareshots: tg.isBoolean,
    has_window_dance: tg.isBoolean,
    tags: tg.isArray(tg.isString),
    sha1: tg.isString,
    rdlevel_sha1: tg.isString
});

export type PrefillResult = LevelBase & {
    image: string
    thumb: string
    url: string 
    icon?: string
}

export const isPrefillResult: tg.TypeGuard<PrefillResult> = tg.isIntersection(isLevelBase, tg.isLikeObject({
    image: tg.isString,
    thumb: tg.isString,
    url: tg.isString,
    icon: tg.isOptional(tg.isString)
}))