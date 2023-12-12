import { search } from "@orchard/api/levels/levels";
import { rdSearchParamsAtom } from "@orchard/stores/rd_search";
import { useAsyncAction } from "./useAsync";
import { useEffect } from "preact/hooks";
import { tuple } from "@orchard/utils/grabbag";

export function useSearchResults() {
    const [searchResults, startSearch] = useAsyncAction(async (get, _set) => {
        const query = get(rdSearchParamsAtom);
        const results = await search(query);
        return results;
    });

    useEffect(() => {
        if (searchResults.state === "not started") {
            startSearch();
        }
    }, [searchResults]);

    return tuple(searchResults, startSearch);
}