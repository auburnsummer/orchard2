import { WithClass } from "~/utils/types"
import cc from "clsx";
import { Link } from "@remix-run/react"

type PublisherHeaderProps = WithClass;

import "./PublisherHeader.css";

export function PublisherHeader({className} : PublisherHeaderProps) {
    return (
        <div className={cc(className, "ph")}>
            <Link to="/">
                <span className="ph_logo">Rhythm Cafe Publisher Interface</span>
            </Link>
            {/* <div aria-hidden className="he_spacer" />
            <div className="he_profile">
                <Profile user={user} />
            </div> */}
        </div>
    )

}