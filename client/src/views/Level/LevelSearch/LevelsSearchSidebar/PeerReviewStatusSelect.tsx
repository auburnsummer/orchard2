import { useSearchParams } from "@cafe/minibridge/hooks";
import { Radio } from "@cafe/components/ui/Radio";
import { Words } from "@cafe/components/ui/Words";
import { useState, useEffect } from "react";

const PEER_REVIEW_STATUSES = [
  { value: "approved", label: "Peer Reviewed" },
  { value: "pending", label: "Pending" },
  { value: "rejected", label: "Non-Referred" },
  { value: "all", label: "All" },
];

export function PeerReviewStatusSelect() {
  const [searchParams, navigateViaSearchParams] = useSearchParams();

  const urlStatus = searchParams.get("peer_review") || "approved";
  const [currentStatus, setCurrentStatus] = useState(urlStatus);

  // Sync local state with URL when it changes
  useEffect(() => {
    setCurrentStatus(urlStatus);
  }, [urlStatus]);

  return (
    <div>
      <Words variant="label" className="mb-2 block">Peer Review Status</Words>
      <div className="flex flex-col gap-0.5">
        {PEER_REVIEW_STATUSES.map((status) => (
          <Radio
            key={status.value}
            name="peer_review"
            label={status.label}
            checked={currentStatus === status.value}
            onChange={() => {
              // Update local state immediately for responsive UI
              setCurrentStatus(status.value);

              navigateViaSearchParams((params) => {
                params.set("peer_review", status.value);
              });
            }}
          />
        ))}
      </div>
    </div>
  );
}
