import { LevelCard } from "@cafe/components/LevelCard/LevelCard"
import { Shell } from "@cafe/components/Shell"
import { RDLevelPrefill, RDLevelPrefillReady } from "@cafe/types/rdLevelPrefill"
import commonStyles from '@cafe/theme/commonPatterns.module.css';
import styles from "./PrefillReady.module.css";
import { Alert, TagsInput, Center, TextInput, Text, Stack, Group, Button, Textarea, NumberInput, Switch, Fieldset, Slider, Checkbox, SimpleGrid, Grid } from "@mantine/core";

import cc from "clsx";
import { useLoggedInUser } from "@cafe/hooks/useUser";
import { useRef, useState } from "react";
import { RDLevel } from "@cafe/types/rdLevelBase";
import { atom, useAtom } from "jotai";

import { withImmer } from "jotai-immer";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faInfoCircle } from "@fortawesome/free-solid-svg-icons";

const CHECKBOXES = [
    ["single_player", "Single Player"],
    ["two_player", "Two Player"],
    ["seizure_warning", "Seizure Warning"],
    ["has_classics", "Has classic beats"],
    ["has_oneshots", "Has Oneshots"],
    ["has_squareshots", "Has Squareshots"],
    ["has_freezeshots", "Has Freezeshots"],
    ["has_freetimes", "Has Freetimes"],
    ["has_holds", "Has Holds"],
    ["has_skipshots", "Skipshots"],
    ["has_window_dance", "Has Window Dance"]
] as const;

function buildInitialLevel(prefill: RDLevelPrefillReady): RDLevel {
    return {
        ...prefill.data,
        song_alt: "",
        submitter: prefill.user,
        club: prefill.club,
        approval: 0
    }
}

type PrefillReadyProps = {
    prefill: RDLevelPrefillReady
}

function PrefillPreview({ level }: { level: RDLevel }) {
    return (
        <Center className={cc(styles.aside, commonStyles.paperBg)}>
            <LevelCard level={level} className={styles.preview} />
        </Center>
    )
}

export function PrefillReady({ prefill }: PrefillReadyProps) {
    const user = useLoggedInUser();
    const prefillAtom = useRef(
        withImmer(
            atom(
                buildInitialLevel(prefill)
            )
        )
    );

    const [level, setLevel] = useAtom(prefillAtom.current);

    const [bpmSync, setBpmSync] = useState(false);

    return (
        <Shell
            aside={<PrefillPreview level={level} />}
        >
            <Stack
                p="md"
                gap="md"
            >
                <Alert icon={<FontAwesomeIcon icon={faInfoCircle} />}>
                    <Text>We've filled out the fields below based on the rdzip file.</Text>
                    <Text>If it all looks OK, you can simply click "Add Level" now to add the level.</Text>
                    <Text>Otherwise, make changes, and then click "Add Level".</Text>
                    <Text>You will be able to come back and edit later.</Text>
                </Alert>
                <Group
                    justify="space-between"
                >
                    <Button
                        onClick={_ => setLevel(buildInitialLevel(prefill))}
                    >
                        Reset
                    </Button>
                    <Button>
                        Add Level
                    </Button>
                </Group>
                <Group
                    align="end"
                >
                    <TextInput
                        label="Song Name"
                        onChange={e => setLevel(l => {
                            l.song = e.target.value;
                        })}
                        value={level.song}
                    >
                    </TextInput>
                    <TextInput
                        label="Song Name (alternate)"
                        value={level.song_alt}
                        onChange={e => setLevel(l => {
                            l.song_alt = e.target.value;
                        })}
                        description="Alternate name of the song, such as a localised or romanized name."
                    />
                </Group>
                <Textarea
                    label="Description"
                    description="Note: <color> tags are not supported. Any <color> tags have been removed."
                    value={level.description}
                    onChange={e => setLevel(l => {
                        l.description = e.target.value;
                    })}
                />
                <TagsInput
                    label="Artists"
                    description="Press [Enter] after typing to add an artist."
                    value={level.artist_tokens}
                    splitChars={[]}
                    onChange={values => setLevel(l => {
                        if (values.length > 0) {
                            l.artist_tokens = values;
                        }
                    })}
                />
                <Fieldset
                    legend="BPM"
                >
                    <Group
                        align="end"
                    >
                        <NumberInput
                            label="Min BPM"
                            value={level.min_bpm}
                            min={0}
                            max={bpmSync ? 1000 : level.max_bpm}
                            onChange={value => setLevel(l => {
                                if (typeof value === "number") {
                                    l.min_bpm = value;
                                    if (bpmSync) {
                                        l.max_bpm = value;
                                    }
                                }
                            })}
                        />
                        <NumberInput
                            label="Max BPM"
                            value={level.max_bpm}
                            min={bpmSync ? 0 : level.min_bpm}
                            max={1000}
                            onChange={value => setLevel(l => {
                                if (typeof value === "number") {
                                    l.max_bpm = value;
                                    if (bpmSync) {
                                        l.min_bpm = value;
                                    }
                                }
                            })}
                        />
                        <Switch
                            checked={bpmSync}
                            onChange={(event) => setBpmSync(event.currentTarget.checked)}
                            label="Sync BPM inputs"
                        >

                        </Switch>
                    </Group>
                </Fieldset>
                <Fieldset legend="Difficulty" pb="xl">
                    <Slider
                        label={null}
                        step={0.001}
                        w={300}
                        min={0}
                        max={3}
                        value={level.difficulty}
                        onChange={value => setLevel(l => {
                            l.difficulty = value;
                        })}
                        restrictToMarks={true}
                        marks={[
                            { value: 0, label: 'Easy' },
                            { value: 1, label: 'Medium' },
                            { value: 2, label: 'Tough' },
                            { value: 3, label: 'Very Tough' }
                        ]}
                    />
                </Fieldset>
                <TagsInput
                    label="Tags"
                    description="Press [Enter] after typing to add an tag."
                    value={level.tags}
                    splitChars={[]}
                    onChange={values => setLevel(l => {
                        if (values.length > 0) {
                            l.tags = values;
                        }
                    })}
                />
                <Fieldset
                    p="md"
                >
                    <Grid
                        justify="flex-start"
                        align="flex-start"
                    >
                        {
                            CHECKBOXES.map(([key, label]) => {
                                return (
                                    <Grid.Col
                                        span={4}
                                    >
                                        <Checkbox
                                            checked={level[key]}
                                            label={label}
                                            onChange={(e) => setLevel(l => {
                                                l[key] = e.target.checked;
                                            })}
                                        />
                                    </Grid.Col>
                                )
                            })
                        }
                    </Grid>
                </Fieldset>


            </Stack>
        </Shell>
    )
}