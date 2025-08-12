import { ConjunctionList } from "@cafe/components/ConjunctionList/ConjunctionList";
import { Shell } from "@cafe/components/Shell";
import { RDLevel } from "@cafe/types/rdLevelBase";
import { faHeartPulse, faPen, faDownload, faLink, faTrash, faEdit, faTags, faUsers, faExclamationTriangle } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Container, Group, Image, Stack, Title, Text, UnstyledButton, Button, Modal, Card, Badge, Grid, Divider, Box, Paper } from "@mantine/core";

import styles from "./LevelView.module.css";
import commonPatterns from "@cafe/theme/commonPatterns.module.css";

import { faDiscord } from "@fortawesome/free-brands-svg-icons";
import { useClipboard, useDisclosure } from "@mantine/hooks";
import { Form } from "@cafe/minibridge/components/Form";
import { Link } from "@cafe/minibridge/components/Link";
import { useCSRFTokenInput } from "@cafe/hooks/useCSRFToken";
import { DIFFICULTY_STRINGS } from "@cafe/utils/constants";

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

    const csrfInput = useCSRFTokenInput();

    // TODO: align with DifficultyDecorator.tsx
    const getDifficultyColor = (difficulty: number) => {
        if (difficulty === 0) return 'green';   // Easy
        if (difficulty === 1) return 'yellow';  // Medium
        if (difficulty === 2) return 'orange';  // Tough
        return 'red';                           // Very Tough
    };

    const getDifficultyString = (difficulty: number) => {
        return DIFFICULTY_STRINGS[difficulty] || 'Unknown';
    };

    return (
        <Shell>
            <Modal
                opened={showDeleteForm}
                onClose={closeDeleteForm}
                title={`Delete ${rdlevel.song}`}
                centered
            >
                <Form
                    method="POST"
                    action={`/levels/${rdlevel.id}/delete/`}
                >
                    {csrfInput}
                    <Stack>
                        <Text>Are you sure you want to delete this level?</Text>
                        <Text c="dimmed" size="sm">This action cannot be undone.</Text>
                        <Group justify="flex-end">
                            <Button variant="default" onClick={closeDeleteForm}>
                                Cancel
                            </Button>
                            <Button type="submit" color="red" leftSection={<FontAwesomeIcon icon={faTrash} />}>
                                Delete Level
                            </Button>
                        </Group>
                    </Stack>
                </Form>
            </Modal>

            <Container size="xl" py="xl">
                <Grid>
                    {/* Main Content */}
                    <Grid.Col span={{ base: 12, md: 8 }}>
                        <Card shadow="sm" padding="lg" radius="md" withBorder>
                            <Group align="flex-start" mb="md">
                                <Image
                                    src={rdlevel.image_url}
                                    alt={`${rdlevel.song} cover`}
                                    radius="md"
                                    h={200}
                                    w={355}
                                    fit="cover"
                                />
                                
                                <Stack flex={1} gap="xs">
                                    <div>
                                        <ConjunctionList
                                            className={styles.artistList}
                                            items={rdlevel.artist_tokens}
                                            elementRender={v => <Text c="dimmed" size="sm">{v}</Text>}
                                            literalRender={v => <Text c="dimmed" size="sm">{v}</Text>}
                                        />
                                        <Title order={1} size="h2" mb="xs">
                                            {rdlevel.song}
                                            {rdlevel.song_alt && (
                                                <Text span c="dimmed" ml="xs">({rdlevel.song_alt})</Text>
                                            )}
                                        </Title>
                                    </div>

                                    <Group gap="md" wrap="wrap">
                                        <Group gap="xs">
                                            <FontAwesomeIcon icon={faPen} className={styles.metaIcon} />
                                            <ConjunctionList
                                                className={styles.metadataList}
                                                elementRender={(v) => 
                                                    typeof v === 'string' 
                                                        ? <UnstyledButton className={styles.authorButton}>{v}</UnstyledButton> 
                                                        : <></>
                                                }
                                                literalRender={(v) => <Text span size="sm">{v}</Text>}
                                                items={rdlevel.authors}
                                            />
                                        </Group>

                                        <Group gap="xs">
                                            <FontAwesomeIcon icon={faHeartPulse} className={styles.metaIcon} />
                                            <Text size="sm">{bpmText}</Text>
                                        </Group>

                                        <Group gap="xs">
                                            <FontAwesomeIcon icon={faDiscord} className={styles.metaIcon} />
                                            <Text size="sm">{rdlevel.club.name}</Text>
                                        </Group>
                                    </Group>

                                    <Group gap="xs" mt="xs">
                                        <Badge 
                                            color={getDifficultyColor(rdlevel.difficulty)} 
                                            variant="light"
                                            size="lg"
                                        >
                                            {getDifficultyString(rdlevel.difficulty)}
                                        </Badge>
                                        
                                        {rdlevel.seizure_warning && (
                                            <Badge color="red" variant="light" leftSection={<FontAwesomeIcon icon={faExclamationTriangle} />}>
                                                Seizure Warning
                                            </Badge>
                                        )}
                                        
                                        {rdlevel.single_player && rdlevel.two_player ? (
                                            <Badge variant="light" leftSection={<FontAwesomeIcon icon={faUsers} />}>
                                                1-2 Players
                                            </Badge>
                                        ) : rdlevel.two_player ? (
                                            <Badge variant="light" leftSection={<FontAwesomeIcon icon={faUsers} />}>
                                                2 Players
                                            </Badge>
                                        ) : (
                                            <Badge variant="light" leftSection={<FontAwesomeIcon icon={faUsers} />}>
                                                1 Player
                                            </Badge>
                                        )}
                                    </Group>
                                </Stack>
                            </Group>

                            <Divider my="md" />

                            {/* Action Buttons */}
                            <Group mb="md">
                                <Button 
                                    component="a" 
                                    href={rdlevel.rdzip_url}
                                    leftSection={<FontAwesomeIcon icon={faDownload} />}
                                    size="md"
                                >
                                    Download
                                </Button>
                                <Button
                                    variant="light"
                                    leftSection={<FontAwesomeIcon icon={faLink} />}
                                    onClick={() => clipboard.copy(rdlevel.rdzip_url)}
                                >
                                    {clipboard.copied ? "Copied!" : "Copy Link"}
                                </Button>
                                {can_edit && (
                                    <Button 
                                        component={Link} 
                                        href={`/levels/${rdlevel.id}/edit/`}
                                        variant="light"
                                        leftSection={<FontAwesomeIcon icon={faEdit} />}
                                    >
                                        Edit
                                    </Button>
                                )}
                                {can_delete && (
                                    <Button
                                        color="red"
                                        variant="light"
                                        leftSection={<FontAwesomeIcon icon={faTrash} />}
                                        onClick={openDeleteForm}
                                    >
                                        Delete
                                    </Button>
                                )}
                            </Group>

                            {/* Description */}
                            {rdlevel.description && (
                                <Box>
                                    <Text fw={500} mb="xs">Description</Text>
                                    <Paper p="md" className={commonPatterns.paperBg}>
                                        {rdlevel.description.split('\n').map((paragraph, index) => (
                                            <Text key={index} mb="xs">{paragraph}</Text>
                                        ))}
                                    </Paper>
                                </Box>
                            )}
                        </Card>
                    </Grid.Col>

                    {/* Sidebar */}
                    <Grid.Col span={{ base: 12, md: 4 }}>
                        <Stack gap="md">
                            {/* Tags */}
                            {rdlevel.tags.length > 0 && (
                                <Card shadow="sm" padding="md" radius="md" withBorder>
                                    <Group gap="xs" mb="xs">
                                        <FontAwesomeIcon icon={faTags} className={styles.sectionIcon} />
                                        <Text fw={500}>Tags</Text>
                                    </Group>
                                    <Group gap="xs">
                                        {rdlevel.tags.map(tag => (
                                            <Badge key={tag} variant="light" size="sm">{tag}</Badge>
                                        ))}
                                    </Group>
                                </Card>
                            )}

                            {/* Game Mechanics */}
                            <Card shadow="sm" padding="md" radius="md" withBorder>
                                <Text fw={500} mb="md">Game Mechanics</Text>
                                <Stack gap="xs">
                                    {rdlevel.has_classics && (
                                        <Group gap="xs">
                                            <Badge color="blue" variant="dot" size="xs" />
                                            <Text size="sm">Classic Beats</Text>
                                        </Group>
                                    )}
                                    {rdlevel.has_oneshots && (
                                        <Group gap="xs">
                                            <Badge color="green" variant="dot" size="xs" />
                                            <Text size="sm">Oneshots</Text>
                                        </Group>
                                    )}
                                    {rdlevel.has_squareshots && (
                                        <Group gap="xs">
                                            <Badge color="orange" variant="dot" size="xs" />
                                            <Text size="sm">Squareshots</Text>
                                        </Group>
                                    )}
                                    {rdlevel.has_freezeshots && (
                                        <Group gap="xs">
                                            <Badge color="cyan" variant="dot" size="xs" />
                                            <Text size="sm">Freezeshots</Text>
                                        </Group>
                                    )}
                                    {rdlevel.has_freetimes && (
                                        <Group gap="xs">
                                            <Badge color="purple" variant="dot" size="xs" />
                                            <Text size="sm">Freetimes</Text>
                                        </Group>
                                    )}
                                    {rdlevel.has_holds && (
                                        <Group gap="xs">
                                            <Badge color="pink" variant="dot" size="xs" />
                                            <Text size="sm">Holds</Text>
                                        </Group>
                                    )}
                                    {rdlevel.has_skipshots && (
                                        <Group gap="xs">
                                            <Badge color="red" variant="dot" size="xs" />
                                            <Text size="sm">Skipshots</Text>
                                        </Group>
                                    )}
                                    {rdlevel.has_window_dance && (
                                        <Group gap="xs">
                                            <Badge color="teal" variant="dot" size="xs" />
                                            <Text size="sm">Window Dance</Text>
                                        </Group>
                                    )}
                                </Stack>
                            </Card>
                        </Stack>
                    </Grid.Col>
                </Grid>
            </Container>
        </Shell>
    );
}