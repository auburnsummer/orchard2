import { RDLevel } from "@cafe/types/rdLevelBase";
import { PeerReviewShell } from "./PeerReviewShell";
import { Surface } from "@cafe/components/ui/Surface";
import { Words } from "@cafe/components/ui/Words";

import prart from "./prart.jpg";

type PeerReviewMainViewProps = {
    levels: RDLevel[];
};

export function PeerReviewMainView({ levels }: PeerReviewMainViewProps) {
    return (
        <PeerReviewShell pendingLevels={levels}>
            <Surface className="m-3 p-4">
                <Words variant="header" className="mb-4">
                    Welcome to Peer Review!
                </Words>
                <img src={prart} alt="Peer Review Art" className="mb-4 rounded-lg shadow-md" />
            </Surface>
        </PeerReviewShell>
    )
}