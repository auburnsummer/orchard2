import { ConjunctionList } from "@cafe/components/ConjunctionList/ConjunctionList";
import { Shell } from "@cafe/components/Shell";
import { RDLevel } from "@cafe/types/rdLevelBase";
import { faHeartPulse, faPen } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Container, Group, Image, Stack, Title, Text, UnstyledButton, Button, Blockquote, Modal } from "@mantine/core";

import styles from "./LevelView.module.css";

import cc from "clsx";
import { faDiscord } from "@fortawesome/free-brands-svg-icons";
import { useClipboard, useDisclosure } from "@mantine/hooks";
import { Form } from "@cafe/minibridge/components/Form";
import { Link } from "@cafe/minibridge/components/Link";

type LevelViewProps = {
    rdlevel: RDLevel,
    can_edit: boolean,
    can_delete: boolean
}

export function LevelView({rdlevel, can_edit, can_delete}: LevelViewProps) {
    const clipboard = useClipboard({ timeout: 500 });
    const bpmText = rdlevel.min_bpm === rdlevel.max_bpm
        ? `${rdlevel.min_bpm} BPM`
        : `${rdlevel.min_bpm}-${rdlevel.max_bpm} BPM`;

    const [showDeleteForm, {open: openDeleteForm, close: closeDeleteForm}] = useDisclosure(false);

    return (
        <Shell>
            <Modal
                opened={showDeleteForm}
                onClose={closeDeleteForm}
                title={`Delete ${rdlevel.song}`}
            >
                <Form
                    method="POST"
                    action={`/levels/${rdlevel.id}/delete`}
                >
                    <Text>Please confirm you want to delete this level by clicking the button.</Text>
                    <Text>Note: this action is irreversible.</Text>
                    <Button type="submit" color="red" variant="outline" mt="md">
                        Delete
                    </Button>
                </Form>
            </Modal>
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
                            <Button component={Link} href={`/levels/${rdlevel.id}/edit`}>
                                Edit
                            </Button>
                        )
                    }
                    {
                        can_delete && (
                            <Button
                                type="submit"
                                color="red"
                                variant="outline"
                                onClick={openDeleteForm}
                            >
                                Delete
                            </Button>
                        )
                    }
                </Group>
                <Blockquote mt="md">
                    {
                        rdlevel.description.split('\n').map((p) => <Text>{p}</Text>)
                    }
                </Blockquote>
                {/* we'll style this later */}
                <dl>
                    <div>
                        <dt>Difficulty</dt>
                        <dd>{rdlevel.difficulty}</dd>
                    </div>
                    <div>
                        <dt>Seizure Warning</dt>
                        <dd>{rdlevel.seizure_warning ? "Yes" : "No"}</dd>
                    </div>
                    <div>
                        <dt>Tags</dt>
                        <dd>{rdlevel.tags.join(", ")}</dd>
                    </div>
                    <div>
                        <dt>Tags</dt>
                        <dd>{rdlevel.tags.join(", ")}</dd>
                    </div>
                    <div>
                        <dt>Has Classics</dt>
                        <dd>{rdlevel.has_classics ? "Yes" : "No"}</dd>
                    </div>
                    <div>
                        <dt>Has One Shots</dt>
                        <dd>{rdlevel.has_oneshots ? "Yes" : "No"}</dd>
                    </div>
                    <div>
                        <dt>Has Square Shots</dt>
                        <dd>{rdlevel.has_squareshots ? "Yes" : "No"}</dd>
                    </div>
                    <div>
                        <dt>Has Freeze Shots</dt>
                        <dd>{rdlevel.has_freezeshots ? "Yes" : "No"}</dd>
                    </div>
                    <div>
                        <dt>Has Free Times</dt>
                        <dd>{rdlevel.has_freetimes ? "Yes" : "No"}</dd>
                    </div>
                    <div>
                        <dt>Has Holds</dt>
                        <dd>{rdlevel.has_holds ? "Yes" : "No"}</dd>
                    </div>
                    <div>
                        <dt>Has Skip Shots</dt>

                        <dd>{rdlevel.has_skipshots ? "Yes" : "No"}</dd>
                    </div>
                    <div>
                        <dt>Has Window Dance</dt>
                        <dd>{rdlevel.has_window_dance ? "Yes" : "No"}</dd>
                    </div>
                    <div>
                        <dt>Single Player</dt>
                        <dd>{rdlevel.single_player ? "Yes" : "No"}</dd>
                    </div>
                    <div>
                        <dt>Two Player</dt>
                        <dd>{rdlevel.two_player ? "Yes" : "No"}</dd>
                    </div>
                </dl>
            </Container>
        </Shell>
    );
}