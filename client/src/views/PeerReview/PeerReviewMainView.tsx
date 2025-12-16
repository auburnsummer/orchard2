import { RDLevel } from "@cafe/types/rdLevelBase";
import { PeerReviewShell } from "./PeerReviewShell";
import { Surface } from "@cafe/components/ui/Surface";
import { Words } from "@cafe/components/ui/Words";

import prart from "./prart.jpg";
import { Checkbox } from "@cafe/components/ui/Checkbox";

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
                    instructions to go here
                </Words>
                <Checkbox
                    label="I agree to receive 238 potatos each month."
                    description="efwefwafwef"
                    showDescriptionAsTooltip={true}
                />
            </Surface>
        </PeerReviewShell>
    )
}