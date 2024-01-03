import { search } from "@orchard/api/levels/levels";
import { DEFAULT_SEARCH_PARAMS, isKeyOfDefaultSearchParams, rdSearchParamsAtom } from "@orchard/stores/rd_search";
import { useAsyncAction2 as useAsyncAction } from "./useAsyncAction";
import { useCallback, useEffect, useMemo } from "preact/hooks";
import { tuple } from "@orchard/utils/grabbag";
import { objectEntries } from 'ts-extras';
import { useAtomValue } from "jotai";

export function useSearchResults() {
    const searchParams = useAtomValue(rdSearchParamsAtom);

    const fetcher = useMemo(() => {
        return async (writeQueryParams: boolean) => {
            if (writeQueryParams) {
                const url = new URL(window.location.href);
                for (const [key, value] of objectEntries(searchParams)) {
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
            const results = await search(searchParams);
            return results;
        }
    }, [searchParams]);

    const [searchResults, startSearchInternal] = useAsyncAction(fetcher);

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