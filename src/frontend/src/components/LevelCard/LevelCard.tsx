import { WithClass } from "@orchard/utils/withClass";
import cc from "clsx";

import "./LevelCard.css";

type LevelCardProps = WithClass;

// just a stub for now.
export function LevelCard({"class": _class}: LevelCardProps) {
    return (
        <div class={cc(_class, "lc")}>

        </div>
    )
}