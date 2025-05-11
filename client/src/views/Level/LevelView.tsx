import { ConjunctionList } from "@cafe/components/ConjunctionList/ConjunctionList";
import { Shell } from "@cafe/components/Shell";
import { RDLevel } from "@cafe/types/rdLevelBase";
import { faHeartPulse, faPen } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Container, Group, Image, Stack, Title, Text, UnstyledButton } from "@mantine/core";

import styles from "./LevelView.module.css";

import cc from "clsx";
import { faDiscord } from "@fortawesome/free-brands-svg-icons";

type LevelViewProps = {
    rdlevel: RDLevel
}

export function LevelView({rdlevel}: LevelViewProps) {
    const bpmText = rdlevel.min_bpm === rdlevel.max_bpm
        ? `${rdlevel.min_bpm} BPM`
        : `${rdlevel.min_bpm}-${rdlevel.max_bpm} BPM`;

    return (
        <Shell>
            <Container pt="md">
                <Group
                    align="flex-start"
                >
                    <Image
                        h={240}
                        w="auto"
                        src={rdlevel.image_url}
                    >
                    </Image>
                    <Stack gap={0}>
                        <ConjunctionList
                            className={styles.artistList}
                            items={rdlevel.artist_tokens}
                            elementRender={v => <p className={styles.artist}>{v}</p>}
                            literalRender={v => <p className={styles.artist}>{v}</p>}
                        />
                        <Group>
                            <Title>{rdlevel.song}</Title>
                            {
                                rdlevel.song_alt && (
                                    <Text>({rdlevel.song_alt})</Text>
                                )
                            }
                        </Group>
                        <Stack pt="xs">
                            <Group>
                                <FontAwesomeIcon icon={faPen} className={styles.topSectionIcon} />
                                <ConjunctionList
                                    className={styles.metadataList}
                                    elementRender={(v) => 
                                        typeof v === 'string' 
                                            ? <UnstyledButton
                                            >
                                                {v}
                                            </UnstyledButton> : <></>
                                    }
                                    literalRender={(v) => <span>{v}</span>}
                                    items={rdlevel.authors}
                                />
                            </Group>
                            <Group>
                                <FontAwesomeIcon icon={faHeartPulse} className={styles.topSectionIcon}  />
                                <Text className={cc(styles.metaitemText, styles.bpmText)}>{bpmText}</Text>
                            </Group>
                            <Group>
                                <FontAwesomeIcon icon={faDiscord} className={styles.topSectionIcon}  />
                                <Text className={cc(styles.metaitemText, styles.bpmText)}>{rdlevel.club.name}</Text>
                            </Group>
                        </Stack>
                    </Stack>
                </Group>
            </Container>
        </Shell>
    );
}