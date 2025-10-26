import { RDLevelPrefill } from "@cafe/types/rdLevelPrefill";
import { PrefillLoading } from "./PrefillLoading";
import { PrefillReady } from "./PrefillReady";
import { PrefillUpdate } from "./PrefillUpdate";
import { RDLevel } from "@cafe/types/rdLevelBase";
import { LevelAlreadyExists } from "./LevelAlreadyExists";

type LevelAddFromPrefillProps = {
  prefill: RDLevelPrefill;
  potential_matches: RDLevel[];
  existing_level: RDLevel | null;
};

export function LevelAddFromPrefill({
  prefill,
  potential_matches,
  existing_level,
}: LevelAddFromPrefillProps) {
  if (prefill.ready) {
    if (existing_level) {
      return <LevelAlreadyExists existingLevel={existing_level} />;
    }
    if (prefill.prefill_type === "new") {
      return <PrefillReady prefill={prefill} />;
    } else {
      return (
        <PrefillUpdate prefill={prefill} potentialMatches={potential_matches} />
      );
    }
  }

  return (
    <PrefillLoading prefillType={prefill.prefill_type} error={prefill.errors} />
  );
}
