import { faExternalLink } from "@fortawesome/free-solid-svg-icons";
import { Words } from "./Words";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

import cc from "clsx";


type ExternalLinkProps = {
    href: string;
    className?: string;
    children?: React.ReactNode;
}

export function ExternalLink({ href, className, children }: ExternalLinkProps) {
    return (
        <Words
            as="a"
            variant="link"
            href={href}
            className={cc("inline-flex items-center mr-1.5", className)}
        >
            <span>{children}</span>
            <FontAwesomeIcon icon={faExternalLink} className="ml-1 text-xs" />
        </Words>
    );
}