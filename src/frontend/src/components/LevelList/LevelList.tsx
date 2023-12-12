import { useEffect } from "preact/hooks";
import "./LevelList.css";
import { search } from "@orchard/api/levels/levels";
import { RDQueryResult, RDSearchParams } from "@orchard/api/levels/types";
import { WithClass } from "@orchard/utils/withClass";
import { useAsyncAction } from "@orchard/hooks/useAsync";
import { useAtom } from "jotai";
import { rdSearchParamsAtom } from "@orchard/stores/rd_search";
import { useSearchResults } from "@orchard/hooks/useSearchResults";

type LevelListProps = WithClass;

export function LevelList({"class": _class}: LevelListProps) {
    const [query, setQuery] = useAtom(rdSearchParamsAtom);

    const [searchResults, startSearch] = useSearchResults();

    if (searchResults.state === "not started") {
        return (
            <div>
            <p>not started</p>
            <button onClick={startSearch}>search</button>
            </div>
        )
    }

    if (searchResults.state === "loading") {
        return (
            <p>loading</p>
        )
    }

    if (searchResults.state === "has error") {
        return (
            <p>error</p>
        )
    }

    return (
        <p>{JSON.stringify(searchResults.data)}</p>
    )
}