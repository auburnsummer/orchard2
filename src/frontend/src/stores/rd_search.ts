/**
 * The current query and result.
 */

import { RDSearchParams } from '@orchard/api/levels/types';
import { atomWithDefault } from 'jotai/utils';

import * as tg from "generic-type-guard";

export const DEFAULT_SEARCH_PARAMS = {
    min_approval: 10
}
type DefaultSearchParamsKeys = keyof (typeof DEFAULT_SEARCH_PARAMS);

export const isKeyOfDefaultSearchParams: tg.TypeGuard<DefaultSearchParamsKeys> = tg.isElementOf("min_approval")

export const rdSearchParamsAtom = atomWithDefault<RDSearchParams>(_ => {
    const searchParams = new URLSearchParams(window.location.search);

    console.log(searchParams);

    const stringGet = (key: string) => searchParams.get(key) || undefined;
    const stringArrGet = (key: string) => {
        const values = searchParams.getAll(key)
        if (values.length === 0) {
            return undefined;
        }
        return values;
    };
    const funcGet = <T extends unknown>(key: string, func: (v: string) => T, fallback?: T) => {
        const value = searchParams.get(key)
        if (!value) {
            return fallback;
        }
        return func(value);

    };
    const floatGet = (key: string, fallback?: number) => funcGet(key, parseFloat, fallback);
    const intGet = (key: string, fallback?: number) => funcGet(key, parseInt, fallback);
    const intArrGet = (key: string) => {
        const values = searchParams.getAll(key)
        if (values.length === 0) {
            return undefined
        }
        return values.map(parseInt);
    };
    const boolGet = (key: string) => funcGet(key, s => s === 'true');
    return {
        q: stringGet("q"),
        tags: stringArrGet("tags"),
        artists: stringArrGet("artists"),
        authors: stringArrGet("authors"),
        min_bpm: floatGet("min_bpm"),
        max_bpm: floatGet("max_bpm"),
        difficulty: intArrGet("difficulty"),
        single_player: boolGet("single_player"),
        two_player: boolGet("two_player"),
        has_classics: boolGet("has_classics"),
        has_oneshots: boolGet("has_oneshots"),
        has_squareshots: boolGet("has_squareshots"),
        has_freezeshots: boolGet("has_freezeshots"),
        has_freetimes: boolGet("has_freetimes"),
        has_holds: boolGet("has_holds"),
        has_skipshots: boolGet("has_skipshots"),
        has_window_dance: boolGet("has_window_dance"),

        uploader: stringGet("uploader"),
        publisher: stringGet("publisher"),
        min_approval: intGet("min_approval", DEFAULT_SEARCH_PARAMS.min_approval),
        max_approval: intGet("max_approval"),

        offset: intGet("offset"),
        limit: intGet("limit")
    }
});