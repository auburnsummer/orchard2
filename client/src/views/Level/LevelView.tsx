import { ConjunctionList } from "@cafe/components/ConjunctionList/ConjunctionList";
import { Shell } from "@cafe/components/Shell";
import { RDLevel } from "@cafe/types/rdLevelBase";
import { faHeartPulse, faPaste, faPen } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Container, Group, Image, Stack, Title, Text, UnstyledButton, Button } from "@mantine/core";

import styles from "./LevelView.module.css";

import cc from "clsx";
import { faDiscord } from "@fortawesome/free-brands-svg-icons";
import { useClipboard } from "@mantine/hooks";

type LevelViewProps = {
    rdlevel: RDLevel,
    can_edit: boolean
}

export function LevelView({rdlevel, can_edit}: LevelViewProps) {
    const clipboard = useClipboard({ timeout: 500 });
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
                <Group pt="xs">
                    <Button component="a" href={rdlevel.rdzip_url}>
                        Download
                    </Button>
                    <Button
                        onClick={() => {
                            clipboard.copy(rdlevel.rdzip_url);
                        }}
                    >
                        {
                            clipboard.copied
                                ? "Copied!"
                                : "Copy link"
                        }
                    </Button>
                    {
                        can_edit && (
                            <Button component="a" href={`/level/${rdlevel.id}/edit`}>
                                Edit
                            </Button>
                        )
                    }
                </Group>
            </Container>
        </Shell>
    );
}