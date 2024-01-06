import { WithClass } from "@orchard/utils/withClass";
import "./SearchBar.css";

import cc from "clsx";
import { useImmerAtom } from "jotai-immer";
import { rdSearchParamsAtom } from "@orchard/stores/rd_search";
import { Button, Input, Icon } from "@orchard/ui";
import { useSearchResults } from "@orchard/hooks/useSearchResults";
import type { TargetedEvent } from "preact/compat";

type SearchBarProps = WithClass;

export function SearchBar({"class": _class}: SearchBarProps) {
    const [searchParams, setSearchParams] = useImmerAtom(rdSearchParamsAtom);
    const [, startSearch] = useSearchResults();

    const onSubmit = (e: TargetedEvent<HTMLFormElement, Event>) => {
        e.preventDefault();
        startSearch();
    }

    return (
        <div class={cc(_class, 'se')}>
            <div class="se_bar">
                <Input
                    value={searchParams.q || ""}
                    onInput={evt => setSearchParams(d => {
                        d.q = evt.currentTarget.value;
                    })}
                    class="se_input"
                    placeholder="Search"
                />
                <Button onClick={startSearch}>
                    <Icon name="search" />
                </Button>
            </div>
        </div>
    )
}