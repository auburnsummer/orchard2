import { search } from "@orchard/api/levels/levels";
import { rdSearchParamsAtom } from "@orchard/stores/rd_search";
import { useAsyncAction } from "./useAsync";

export function useSearchResults() {
    return useAsyncAction(async (get, _set) => {
        const query = get(rdSearchParamsAtom);
        const results = await search(query);
        return results;
    });
}