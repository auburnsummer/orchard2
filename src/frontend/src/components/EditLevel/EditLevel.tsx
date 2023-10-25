import { VitalsLevelExport } from "@orchard/api/levels"
import { WithClass } from "@orchard/utils/withClass";

import cc from "clsx";

import "./EditLevel.css";
import { Input, Select, TagInput, Textarea, Option, Checkbox } from "@orchard/ui";
import { useRef } from "preact/hooks";
import { atomWithReset } from "jotai/utils";
import { useAtom } from "jotai";

type EditLevelProps = WithClass & {
    levelPrefill: VitalsLevelExport;
}

export function EditLevel({"class": _class, levelPrefill}: EditLevelProps) {
    const levelAtom = useRef(atomWithReset(levelPrefill));

    const [levelPreview, setLevelPreview] = useAtom(levelAtom.current);

    return (
        <div class={cc(_class, "el")}>
            <div class="el_too-small">
                <p class="el_too-small-message">Please increase the size of the web browser</p>
            </div>
            <div class="el_wrapper">
                <form class="el_form">
                    <div class="el_titles">
                        <Input label="Song" value={levelPreview.song} class="el_title"/>
                        <Input label="Song alternative name (optional)" class="el_title" />
                    </div>
                    <TagInput
                        class="el_artists"
                        items={levelPreview.artist_tokens}
                        onItems={items => {
                            setLevelPreview(prev => ({
                                ...prev,
                                artist_tokens: items
                            }));
                        }}
                        commaSubmits={false}
                        inputProps={{
                            label: levelPreview.artist_tokens.length === 1 ? "Artist" : "Artists"
                        }}
                    />
                    <TagInput
                        class="el_authors"
                        items={levelPreview.authors}
                        onItems={items => {
                            setLevelPreview(prev => ({
                                ...prev,
                                artist_tokens: items
                            }));
                        }}
                        commaSubmits={false}
                        inputProps={{
                            label: levelPreview.authors.length === 1 ? "Author" : "Authors"
                        }}
                    />
                    <Textarea
                        class="el_description"
                        value={levelPreview.description}
                        label="Description"
                    />
                    <div class="el_bpm-and-difficulty-section">
                        <Input
                            class="el_bpm"
                            value={`${levelPreview.max_bpm}`}
                            type="number"
                            label="Max BPM"
                        />
                        <Input
                            class="el_bpm"
                            value={`${levelPreview.max_bpm}`}
                            type="number"
                            label="Min BPM"
                        />
                        <Select
                            label="Difficulty"
                            value={`${levelPreview.difficulty}`}
                            class="el_difficulty"
                        >
                            <Option value="0">Easy</Option>
                            <Option value="1">Medium</Option>
                            <Option value="2">Tough</Option>
                            <Option value="3">Very Tough</Option>
                        </Select>
                    </div>
                    <TagInput
                        class="el_tags"
                        items={levelPreview.tags}
                        onItems={items => {
                            setLevelPreview(prev => ({
                                ...prev,
                                tags: items
                            }));
                        }}
                        commaSubmits={true}
                        inputProps={{
                            label: "Tags"
                        }}
                    />
                    <div class="el_checkboxes">
                        <Checkbox
                            checked={levelPreview.seizure_warning}
                        >
                            Seizure warning
                        </Checkbox>
                        <Checkbox
                            checked={levelPreview.single_player}
                        >
                            Supports single player
                        </Checkbox>
                        <p>(for two-handed levels intended to be played by one person, also check this.)</p>
                        <Checkbox
                            checked={levelPreview.two_player}
                        >
                            Supports two player
                        </Checkbox>
                        {
                            [
                                "Classics",
                                "Oneshots",
                                "Squareshots",
                                "Freezeshots",
                                "Freetimes",
                                "Holds",
                                "Skipshots",
                                "Window Dance"
                            ].map(s => (
                                <Checkbox>Has {s}</Checkbox>
                            ))
                        }
                    </div>
                </form>
                <div class="el_preview">

                </div>
            </div>
        </div>
    )
}