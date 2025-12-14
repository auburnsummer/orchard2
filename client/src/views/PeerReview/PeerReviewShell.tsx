import { Shell } from "@cafe/components/Shell";
import { Surface } from "@cafe/components/ui/Surface";
import { RDLevel } from "@cafe/types/rdLevelBase"

type PeerReviewShellProps = {
    pendingLevels: RDLevel[];
    children?: React.ReactNode;
};

function PeerReviewNavbar({pendingLevels}: PeerReviewShellProps) {
    console.log(pendingLevels);
    return (
        <Surface className="m-3">
            <p>fefe</p>
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