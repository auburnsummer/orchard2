import { useSearchParams } from "@cafe/minibridge/hooks";
import { Text, Stack, Radio } from "@mantine/core";
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
      <Text fw={700}>Peer Review Status</Text>
      <Stack gap="0.125rem">
        {PEER_REVIEW_STATUSES.map((status) => (
          <Radio
            key={status.value}
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
      </Stack>
    </div>
  );
}
