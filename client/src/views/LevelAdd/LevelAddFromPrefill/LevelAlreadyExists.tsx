import { LevelCard } from "@cafe/components/LevelCard/LevelCard";
import { ShellDramaticCenter } from "@cafe/components/ShellDramaticCenter";
import { RDLevel } from "@cafe/types/rdLevelBase";

import { Words } from "@cafe/components/ui/Words";

type LevelAlreadyExistsProps = {
  existingLevel: RDLevel;
};

export function LevelAlreadyExists({ existingLevel }: LevelAlreadyExistsProps) {
  return (
    <ShellDramaticCenter>
      <Words as="h2" variant="header">Level Already Exists</Words>
      <Words>This rdzip has already been uploaded:</Words>
      <LevelCard
        level={existingLevel}
        className="mt-4"
        showId={true}
        href={`/levels/${existingLevel.id}/`}
      />
    </ShellDramaticCenter>
  );
}
