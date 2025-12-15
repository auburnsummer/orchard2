import { Shell } from "@cafe/components/Shell";
import { NavEntry } from "@cafe/components/ui/NavEntry";
import { Surface } from "@cafe/components/ui/Surface";
import { Words } from "@cafe/components/ui/Words";
import { locationAtom } from "@cafe/minibridge/atoms";
import { Link } from "@cafe/minibridge/components/Link";
import { RDLevel } from "@cafe/types/rdLevelBase"
import { useAtomValue } from "jotai";

import { useIsConfigured } from "./PeerReviewConfiguration";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faWarning } from "@fortawesome/free-solid-svg-icons";

type PeerReviewShellProps = {
    pendingLevels: RDLevel[];
    children?: React.ReactNode;
};

function PeerReviewNavbar({pendingLevels}: PeerReviewShellProps) {
    const { pathname } = useAtomValue(locationAtom);

    const isConfigured = useIsConfigured();

    return (
        <Surface className="m-3 py-2 flex-grow">
            <Words variant="subheader" className="px-4 mb-2 pb-2">
                Levels {pendingLevels.length > 0 ? `(${pendingLevels.length} pending)` : "No pending reviews"}
            </Words>
            <NavEntry as={Link} href="/peer-review/" active={pathname === "/peer-review/"}>
                Home
            </NavEntry>
            <NavEntry as={Link} href="/peer-review/config/" active={pathname === "/peer-review/config/"}>
                Configuration
                {!isConfigured && (
                    <FontAwesomeIcon icon={faWarning} className="ml-2 text-yellow-500" title="Peer Review is not configured yet!" />
                )}
            </NavEntry>
            {pendingLevels.length > 0 && <hr className="my-2 mx-4 border-t border-gray-300 dark:border-gray-700" />}
            {
                pendingLevels.map((level) => (
                    <NavEntry 
                        key={level.id}
                        as={Link}
                        href={`/peer-review/${level.id}/`}
                        active={pathname === `/peer-review/${level.id}/`}
                    >
                        {level.song}
                    </NavEntry>
                ))
            }
        </Surface>
    )
}

export function PeerReviewShell({ pendingLevels, children }: PeerReviewShellProps) {
    return (
        <Shell
            navbar={
                <PeerReviewNavbar pendingLevels={pendingLevels} />
            }
        >
            {children}
        </Shell>
    )
}