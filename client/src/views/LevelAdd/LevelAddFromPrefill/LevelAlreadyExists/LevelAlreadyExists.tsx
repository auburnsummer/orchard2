import { LevelCard } from "@cafe/components/LevelCard/LevelCard";
import { ShellDramaticCenter } from "@cafe/components/ShellDramaticCenter/ShellDramaticCenter";
import { RDLevel } from "@cafe/types/rdLevelBase";
import { Paper, Title, Text } from "@mantine/core";

import styles from "./LevelAlreadyExists.module.css";

type LevelAlreadyExistsProps = {
  existingLevel: RDLevel;
};

export function LevelAlreadyExists({ existingLevel }: LevelAlreadyExistsProps) {
  return (
    <ShellDramaticCenter>
      <Paper shadow="md" p="xl">
        <Title order={2}>Level Already Exists</Title>
        <Text>This rdzip has already been uploaded:</Text>
        <LevelCard
          level={existingLevel}
          className={styles.level}
          showId={true}
          href={`/levels/${existingLevel.id}/`}
        />
      </Paper>
    </ShellDramaticCenter>
  );
}
