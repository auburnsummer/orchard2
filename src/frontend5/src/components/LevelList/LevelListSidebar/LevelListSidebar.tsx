import { WithClass } from "@orchard/utils/withClass";
import "./LevelListSidebar.css";

import cc from "clsx";

type LevelListSidebarProps = WithClass;

export function LevelListSidebar({"class": _class}: LevelListSidebarProps) {
    return (
        <div class={cc(_class, "ls")}>
            Level list sidebar
        </div>
    )
}