import { search } from "@orchard/api/levels/levels";
import { DEFAULT_SEARCH_PARAMS, isKeyOfDefaultSearchParams, rdSearchParamsAtom } from "@orchard/stores/rd_search";
import { useAsyncAction } from "./useAsync";
import { useCallback, useEffect } from "preact/hooks";
import { tuple } from "@orchard/utils/grabbag";
import { objectEntries } from 'ts-extras';

export function useSearchResults() {
    const [searchResults, startSearchInternal] = useAsyncAction(async (get, _set, writeQueryParams: boolean) => {
        const query = get(rdSearchParamsAtom);
        if (writeQueryParams) {
            const url = new URL(window.location.href);
            for (const [key, value] of objectEntries(query)) {
                if (value == undefined) {
                    continue;
                }
                if (isKeyOfDefaultSearchParams(key)) {
                    if (`${DEFAULT_SEARCH_PARAMS[key]}` == `${value}`) {
                        continue; // don't write this one to query params because it's the same as default.
                    }
                }
                url.searchParams.set(key, `${value}`);
            }
            window.history.pushState({}, '', url);
        }
        const results = await search(query);
        return results;
    });

    useEffect(() => {
        if (searchResults.state === "not started") {
            startSearchInternal(false);
        }
    }, [searchResults]);

    const startSearch = useCallback(() => {
        startSearchInternal(true);
    }, [startSearchInternal]);

    return tuple(searchResults, startSearch);
}