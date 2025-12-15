import { NavEntry } from "@cafe/components/ui/NavEntry";
import { Link } from "@cafe/minibridge/components/Link";
import { RDLevel } from "@cafe/types/rdLevelBase";
import { useState } from "react";

type PendingLevelNavItemProps = {
    level: RDLevel;
    href: string;
    active: boolean;
};

function joinWithAnd(array: string[]): string {
    const formatter = new Intl.ListFormat('en', { style: 'long', type: 'conjunction' });
    return formatter.format(array);
}

export function PendingLevelNavItem({ level, href, active }: PendingLevelNavItemProps) {
    const [isHovered, setIsHovered] = useState(false);

    return (
        <NavEntry
            as={Link}
            href={href}
            active={active}
            onMouseEnter={() => setIsHovered(true)}
            onMouseLeave={() => setIsHovered(false)}
            className="relative overflow-hidden h-16"
        >
            {/* Background image on hover */}
            {isHovered && (
                <div
                    className="absolute inset-0 opacity-20 z-0"
                    style={{
                        backgroundImage: `url('${level.image_url}')`,
                        backgroundSize: 'cover',
                        backgroundPosition: 'center',
                    }}
                />
            )}

            {/* Content */}
            <div className="relative z-10 flex flex-col">
                <div className="font-semibold">{level.song}</div>
                <div className="text-xs opacity-70 mt-0.5">
                    {level.authors.length > 1 ? '👥' : '👤'} {joinWithAnd(level.authors)}
                </div>
            </div>
        </NavEntry>
    );
}
