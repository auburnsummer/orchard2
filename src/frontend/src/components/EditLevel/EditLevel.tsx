import { VitalsLevelExport } from "@orchard/api/levels"
import { WithClass } from "@orchard/utils/withClass";

import cc from "clsx";

import "./EditLevel.css";
import { Input, Select, TagInput, Textarea, Option, Checkbox, Button, Divider, Dialog } from "@orchard/ui";
import { useRef } from "preact/hooks";
import { RESET, atomWithReset } from "jotai/utils";
import { useAtom } from "jotai";
import { withImmer } from "jotai-immer";
import type { User } from "@orchard/api/auth";
import type { Publisher } from "@orchard/api/publisher";
import { useLog } from "@orchard/hooks/useLog";
import type { SlDialog } from "@shoelace-style/shoelace";
import { LevelBox } from "../LevelBox";

type EditLevelProps = WithClass & {
    levelPrefill: VitalsLevelExport;
}

export type LevelPreviewData = VitalsLevelExport & {
    "song_altname": string;
    "publisher": Publisher;
}

function makeInitialAtom(prefill: VitalsLevelExport) {
    const initialLevelState: LevelPreviewData = {
        ...prefill,
        "song_altname": "",
        "publisher": {
            "id": "fakeid",
            "name": "Lorem Ipsum Club"  // TODO: fetch actual publisher from token...
        }
    }
    return withImmer(atomWithReset(initialLevelState));
}

export function EditLevel({"class": _class, levelPrefill}: EditLevelProps) {
    const levelAtom = useRef(makeInitialAtom(levelPrefill));

    const [preview, setPreview] = useAtom(levelAtom.current);

    const levelPreviewDialog = useRef<SlDialog | null>(null);

    useLog(preview);

    return (
        <div class={cc(_class, "el")}>
            <Dialog
                class="el_level-preview-smallscreens"
                ref={levelPreviewDialog}
            >
                <LevelBox level={preview} />
            </Dialog>
            <div class="el_too-small">
                <p class="el_too-small-message">Please increase the size of the web browser</p>
            </div>
            <div class="el_wrapper">
                {/*
                    nit: we should make this an actual form at some point. the current issue is that 
                    TagInput does not behave like a form control
                */}
                <div class="el_form">
                    <div class="el_controls">
                        <Button
                            class="el_reset-button"
                            variant="text"
                            size={"small" as any}
                            onClick={() => setPreview(_ => RESET)}
                        >
                            Reset form
                        </Button>
                        <div class="el_controls-spacer" />
                        <Button
                            class="el_preview-button"
                            onClick={() => {
                                levelPreviewDialog.current?.show();
                            }}
                        >
                            Show preview
                        </Button>
                        {/* not type submit, it's too easy for a stray enter to submit the form */}
                        <Button
                            class="el_submit-button"
                        >
                            Submit
                        </Button>
                    </div>
                    <Divider class="el_control-title-divider" />
                    <div class="el_titles">
                        <Input
                            class="el_title"
                            label="Song"
                            value={preview.song}
                            onSlInput={e => setPreview(d => {
                                d.song = e.target.value;
                            })}
                        />
                        <Input
                            class="el_title"
                            label="Song alternate name (optional)"
                            value={preview.song_altname}
                            onSlInput={e => setPreview(d => {
                                d.song_altname = e.target.value;
                            })}
                        />
                    </div>
                    <TagInput
                        class="el_artists"
                        items={preview.artist_tokens}
                        onItems={items => setPreview(d => {
                            d.artist_tokens = items;
                        })}
                        commaSubmits={false}
                        inputProps={{
                            label: preview.artist_tokens.length === 1 ? "Artist" : "Artists"
                        }}
                    />
                    <TagInput
                        class="el_authors"
                        items={preview.authors}
                        onItems={items => setPreview(d => {
                            d.authors = items;
                        })}
                        commaSubmits={true}
                        inputProps={{
                            label: preview.authors.length === 1 ? "Author" : "Authors"
                        }}
                    />
                    <Textarea
                        class="el_description"
                        value={preview.description}
                        label="Description"
                        onSlInput={e => setPreview(d => {
                            d.description = e.target.value;
                        })}
                    />
                    <div class="el_bpm-and-difficulty-section">
                        <Input
                            class="el_bpm"
                            step="any"
                            value={`${preview.min_bpm}`}
                            type="number"
                            label="Min BPM"
                            onSlInput={e => setPreview(d => {
                                d.min_bpm = parseFloat(e.target.value);
                                if (d.max_bpm < d.min_bpm) {
                                    d.max_bpm = d.min_bpm;
                                }
                            })}
                        />
                        <Input
                            class="el_bpm"
                            step="any"
                            value={`${preview.max_bpm}`}
                            type="number"
                            label="Max BPM"
                            onSlInput={e => setPreview(d => {
                                d.max_bpm = parseFloat(e.target.value);
                                if (d.min_bpm > d.max_bpm) {
                                    d.min_bpm = d.max_bpm;
                                }
                            })}
                        />
                        <Select
                            label="Difficulty"
                            value={`${preview.difficulty}`}
                            class="el_difficulty"
                            onSlChange={e => setPreview(d => {
                                d.difficulty = parseInt(e.target.value);
                            })}
                        >
                            <Option value="0">Easy</Option>
                            <Option value="1">Medium</Option>
                            <Option value="2">Tough</Option>
                            <Option value="3">Very Tough</Option>
                        </Select>
                    </div>
                    <TagInput
                        class="el_tags"
                        items={preview.tags}
                        onItems={items => setPreview(d => {
                            d.tags = items;
                        })}
                        commaSubmits={true}
                        inputProps={{
                            label: "Tags"
                        }}
                    />
                    <div class="el_checkboxes">
                        <Checkbox
                            checked={preview.seizure_warning}
                            onSlInput={e => setPreview(d => {
                                d.seizure_warning = e.target.checked;
                            })}
                        >
                            Seizure warning
                        </Checkbox>
                        <Checkbox
                            checked={preview.single_player}
                            onSlInput={e => setPreview(d => {
                                d.single_player = e.target.checked;
                            })}
                        >
                            Supports single player
                        </Checkbox>
                        <Checkbox
                            checked={preview.two_player}
                            onSlInput={e => setPreview(d => {
                                d.two_player = e.target.checked;
                            })}
                        >
                            Supports two player
                        </Checkbox>
                        {
                            ([
                                ["classics", "Contains classics"],
                                ["oneshots", "Contains oneshots"],
                                ["squareshots", "Contains squareshots"],
                                ["freezeshots", "Contains freezeshots"],
                                ["freetimes", "Contains freetimes"],
                                ["holds", "Contains holds"],
                                ["skipshots", "Contains skipshots"],
                                ["window_dance", "Uses window dance"]
                            ] as const).map(([tag, s]) => {
                                return (
                                    <Checkbox
                                        checked={preview[`has_${tag}`]}
                                        onSlInput={e => setPreview(d => {
                                            d[`has_${tag}`] = e.target.checked;
                                        })}
                                    >
                                        {s}
                                    </Checkbox>
                                )
                            })
                        }
                    </div>
                </div>
                <div class="el_preview">

                </div>
            </div>
        </div>
    )
}