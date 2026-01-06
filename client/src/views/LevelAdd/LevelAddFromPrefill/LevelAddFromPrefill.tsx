import { RDLevelPrefill } from "@cafe/types/rdLevelPrefill";
import { PrefillLoading } from "./PrefillLoading";
import { PrefillReady } from "./PrefillReady";
import { PrefillUpdate } from "./PrefillUpdate";
import { RDLevel } from "@cafe/types/rdLevelBase";
import { LevelAlreadyExists } from "./LevelAlreadyExists";
import { useEffect } from "react";
import { useSetAtom } from "jotai";
import { navigateAtom } from "@cafe/minibridge/atoms";

type LevelAddFromPrefillProps = {
  prefill: RDLevelPrefill;
  potential_matches: RDLevel[];
  existing_level: RDLevel | null;
};

function RedirectTo({url}: {url: URL}) {
  const navigate = useSetAtom(navigateAtom);

  useEffect(() => {
    navigate(url);
  }, []);

  return null;
}

export function LevelAddFromPrefill({
  prefill,
  potential_matches,
  existing_level,
}: LevelAddFromPrefillProps) {
  if (!prefill.ready ){
    return (
      <PrefillLoading prefillType={prefill.prefill_type} error={prefill.errors} />
    );
  }
  if (prefill.prefill_type === "update") {
    return (
      <PrefillUpdate prefill={prefill} potentialMatches={potential_matches} />
    );
  }
  if (prefill.go_to_prepost == false) {
    return <RedirectTo url={new URL(`/levels/${prefill.level_id}/`, window.location.origin)} />
  }

  if (existing_level) {
    return <LevelAlreadyExists existingLevel={existing_level} />;
  }

  return <PrefillReady prefill={prefill} />;
}
