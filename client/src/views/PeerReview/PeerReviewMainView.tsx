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
                <img src={prart} alt="Peer Review Art" className="mb-4 w-md" title="Art by @fruit-sy on Tumblr" />
                <Words variant="muted" as="p">
                    (Art by @fruit-sy on Tumblr)
                </Words>
                <Words variant="subheader">
                    Instructions
                </Words>
                <Words as="p">
                    1. Go to the Configuration page and fill out the two webhook URLs. A token is no longer required.
                </Words>
                <Words as="p">
                    2. Click on a level from the list to review it.
                </Words>
            </Surface>
        </PeerReviewShell>
    )
}