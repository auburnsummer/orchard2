import { Shell } from "@cafe/components/Shell";
import { Words } from "@cafe/components/ui/Words";
import { Navbar } from "@cafe/components/ui/Navbar";
import { RDLevel } from "@cafe/types/rdLevelBase"
import { useAtomValue } from "jotai";
import { locationAtom } from "@cafe/minibridge/atoms";

import { useIsConfigured } from "./PeerReviewConfiguration";
import { PendingLevelNavItem } from "./PendingLevelNavItem";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faWarning } from "@fortawesome/free-solid-svg-icons";

type PeerReviewShellProps = {
    pendingLevels: RDLevel[];
    children?: React.ReactNode;
};

function PeerReviewNavbar({pendingLevels}: PeerReviewShellProps) {
    const { pathname } = useAtomValue(locationAtom);

    const isConfigured = useIsConfigured();

    const links = [
        {
            label: "Home",
            href: "/peer-review/",
        },
        {
            label: (
                <>
                    Configuration
                    {!isConfigured && (
                        <FontAwesomeIcon icon={faWarning} className="ml-2 text-yellow-500" title="Peer Review is not configured yet!" />
                    )}
                </>
            ),
            href: "/peer-review/config/",
        },
        {
            label: "Encrypted Webhook Maker",
            href: "/peer-review/make-encrypted-webhook/",
        },
    ];

    return (
        <Navbar
            links={links}
            className="py-2"
            beforeLinks={
                <Words variant="subheader" className="px-4 mb-2 pb-2">
                    Levels {pendingLevels.length > 0 ? `(${pendingLevels.length} pending)` : "No pending reviews"}
                </Words>
            }
            afterLinks={
                <>
                    {pendingLevels.length > 0 && <hr className="my-2 mx-4 border-t border-gray-300 dark:border-gray-700" />}
                    {
                        pendingLevels.map((level) => (
                            <PendingLevelNavItem
                                key={level.id}
                                level={level}
                                href={`/peer-review/${level.id}/`}
                                active={pathname === `/peer-review/${level.id}/`}
                            />
                        ))
                    }
                </>
            }
        />
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