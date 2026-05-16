import { useDisclosure } from "@mantine/hooks";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPen } from "@fortawesome/free-solid-svg-icons";
import { Link } from "@cafe/minibridge/components/Link";
import { Surface } from "@cafe/components/ui/Surface";
import { Words } from "@cafe/components/ui/Words";

type PeerReviewStatusCardProps = {
  approval: number;
  approval_notes_public: string;
  canPeerReview: boolean;
  levelId: string;
};

export function PeerReviewStatusCard({
  approval,
  approval_notes_public,
  canPeerReview,
  levelId,
}: PeerReviewStatusCardProps) {
  const [showNotes, { toggle }] = useDisclosure(false);

  const statusText =
    approval === 10
      ? "Peer Reviewed"
      : approval === -1
        ? "Non-Refereed"
        : "Pending Peer Review";

  const toggleLabel =
    approval === -1
      ? showNotes ? "Hide reasons" : "Show reasons"
      : showNotes ? "Hide notes" : "Show notes";

  const showToggle = (approval === 10 || approval === -1) && approval_notes_public;

  return (
    <Surface className="p-4">
      <div className="flex items-center gap-1 mb-2">
        <FontAwesomeIcon
          className="text-slate-700 dark:text-slate-300"
          icon={faPen}
        />
        <Words className="font-medium ml-1">Peer Review Status</Words>
      </div>
      <div className="flex flex-col">
        <div className="flex flex-row align-top">
          <Words variant="sm">{statusText}</Words>
          {showToggle && (
            <Words variant="link" as="button" onClick={toggle} className="ml-2 text-xs">
              ({toggleLabel})
            </Words>
          )}
        </div>
        {showNotes && approval_notes_public && (
          <>
            {approval_notes_public.split("\n").map((paragraph, index) => (
              <Words as="p" key={index} variant="muted" className="text-sm mt-1 whitespace-pre-wrap">
                {paragraph}
              </Words>
            ))}
          </>
        )}
      </div>
      {canPeerReview && (
        <Words variant="link" as={Link} href={`/peer-review/${levelId}/`} className="mt-2 block text-sm">
          Go to PR Page for this level
        </Words>
      )}
    </Surface>
  );
}
