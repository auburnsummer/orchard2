import { WithClass } from "@orchard/utils/withClass";
import "./Loading.css";

import cc from "clsx";
import { Spinner } from "@orchard/ui";

type LoadingProps = WithClass & {
    text: string;
}

export function Loading({"class": _class, text}: LoadingProps) {
    return (
        <div class={cc(_class, "lo")}>
            <Spinner class="lo_spinner" />
            <span class="lo_text">{text}</span>
        </div>
    )
}