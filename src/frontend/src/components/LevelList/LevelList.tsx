import "./LevelList.css";
import { WithClass } from "@orchard/utils/withClass";
import { useAtom } from "jotai";
import { rdSearchParamsAtom } from "@orchard/stores/rd_search";
import { useSearchResults } from "@orchard/hooks/useSearchResults";

import cc from "clsx";
import { LevelBox } from "../LevelBox";
import { LevelListSidebar } from "./LevelListSidebar";

type LevelListProps = WithClass;

export function LevelList({"class": _class}: LevelListProps) {
    const [query, setQuery] = useAtom(rdSearchParamsAtom);

    const [searchResults, startSearch] = useSearchResults();

    if (searchResults.state === "not started") {
        // useSearchResults always starts the search automatically.
        // so this state shouldn't ever be rendered.
        return (
            <p>search did not start. if you see this, it's a bug, ping auburn!</p>
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
        <div class={cc(_class, "le")}>
            <LevelListSidebar class="le_sidebar" />
            <ul class="le_levels">
                {
                    searchResults.data.levels.map(level => {
                        return (
                            <LevelBox level={level} key={level.id} class="le_level" />
                        )
                    })
                }
            </ul>
        </div>
    )
}