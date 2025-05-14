import { RDLevel } from "@cafe/types/rdLevelBase";
import { atom, useAtom } from "jotai";
import { useRef, useState } from "react";
import { withImmer } from "jotai-immer";
import { useCSRFTokenInput } from "@cafe/hooks/useCSRFToken";
import { Shell } from "../Shell";

import commonStyles from '@cafe/theme/commonPatterns.module.css';
import styles from "./EditLevelForm.module.css";

import cc from "clsx";
import { Button, Center, Checkbox, Fieldset, Grid, Group, NumberInput, Slider, Stack, Switch, TagsInput, Textarea, TextInput } from "@mantine/core";
import { LevelCard } from "../LevelCard/LevelCard";
import { Form } from "@cafe/minibridge/components/Form";

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


type EditLevelFormProps = {
    level: RDLevel;
    preamble: React.ReactNode;
    submitButtonText: string;
    // form submit url
    // preamble html element to go before the form
}

function PrefillPreview({ level }: { level: RDLevel }) {
    return (
        <Center className={cc(styles.aside, commonStyles.paperBg)}>
            <LevelCard level={level} className={styles.preview} />
        </Center>
    )
}

export function EditLevelForm({level: initialLevel, preamble, submitButtonText}: EditLevelFormProps) {
    const levelAtom = useRef(
        withImmer(
            atom(
                initialLevel
            )
        )
    );
    const csrfInput = useCSRFTokenInput();
    const [level, setLevel] = useAtom(levelAtom.current);
    const [bpmSync, setBpmSync] = useState(false);

    return (
        <Shell
            aside={<PrefillPreview level={level} />}
        >
            <Stack
                p="md"
                gap="md"
            >
                {preamble}
                <Group
                    justify="space-between"
                >
                    <Button
                        onClick={_ => setLevel(initialLevel)}
                    >
                        Reset
                    </Button>
                    {/* the addlevel button is a secret form.
                     since we have some 'exotic' inputs from mantine that don't natively output formdata,
                     instead we have a hidden input with the edited prefill as json.
                    */}
                    <Form
                        method="POST"
                    >
                        {csrfInput}
                        <input type="hidden" name="prefill" value={JSON.stringify(level)} />
                        <Button
                            type="submit"
                        >
                            {submitButtonText}
                        </Button>
                    </Form>
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