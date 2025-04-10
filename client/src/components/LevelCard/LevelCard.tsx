import { RDLevel } from "@cafe/types/rdLevelBase"
import { Card, Image, Stack, Title, Text } from "@mantine/core";

import styles from "./LevelCard.module.css";

type LevelCardProps = {
    level: RDLevel;
}

export function LevelCard({level}: LevelCardProps) {
    return (
        <Card shadow="sm" radius="md" p={0}>
            <Card.Section>
                <Image
                    src={level.thumb_url}
                />
            </Card.Section>
            <Card.Section>
                <Stack className={styles.titleArea}>
                    <Title order={1} className={styles.songName}>{level.song}</Title>
                    <Text c="h2" className={styles.artistName}>{level.artist}</Text>
                </Stack>
            </Card.Section>
        </Card>
    )
}