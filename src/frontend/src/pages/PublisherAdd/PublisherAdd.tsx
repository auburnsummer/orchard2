import { authTokenAtom, useLoggedInUser } from "@orchard/stores/auth";
import "./PublisherAdd.css";
import { Loading } from "@orchard/components/Loading";
import { Header } from "@orchard/components/Header";
import { atom, useAtom } from "jotai";
import { useAsyncAction } from "@orchard/hooks/useAsync";
import { VitalsLevelExport, getLevelPrefill } from "@orchard/api/levels";
import { useEffect, useRef } from "preact/hooks";
import { Button, Checkbox, Input, Select, TagInput, Textarea, Option } from "@orchard/ui";
import { atomWithReset } from "jotai/utils";

type STATES = "prefill"

const stateAtom = atom<STATES>("prefill");

type PublisherAddFormProps = {
    level: VitalsLevelExport
}

function PublisherAddForm({level}: PublisherAddFormProps) {
    const levelAtom = useRef(atomWithReset(level));

    const [levelPreview, setLevelPreview] = useAtom(levelAtom.current);

    return (
        <div class="pa_form-wrapper">
            <div class="pa_form-wrapper2">
                <form class="pa_form">
                    <div class="pa_form-song-section">
                        <Input label="Song" value={level.song}/>
                        <Input label="Song alternate title (optional)" />
                    </div>
                    <TagInput
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
                        value={levelPreview.description}
                        label="Description"
                    />
                    <div class="pa_form-bpm-and-difficulty-section">
                        <Input
                            class="pa_form-bpm"
                            value={`${levelPreview.max_bpm}`}
                            type="number"
                            label="Max BPM"
                        />
                        <Input
                            class="pa_form-bpm"
                            value={`${levelPreview.max_bpm}`}
                            type="number"
                            label="Min BPM"
                        />
                        <Select
                            label="Difficulty"
                            value={`${levelPreview.difficulty}`}
                            class="pa_form-difficulty"
                        >
                            <Option value="0">Easy</Option>
                            <Option value="1">Medium</Option>
                            <Option value="2">Tough</Option>
                            <Option value="3">Very Tough</Option>
                        </Select>
                    </div>
                    <TagInput
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
                </form>
            </div>
            <div class="pa_preview">

            </div>
        </div>
    )
}

function PublisherAddMainPhase() {
    const [state, setState] = useAtom(stateAtom);
    
    const [prefillResult, startPrefill] = useAsyncAction(async (get, _set, publisherToken: string | null) => {
        if (publisherToken == null) {
            throw new Error("No publisher token given. Try the command again in discord")
        }
        const userToken = get(authTokenAtom);
        return getLevelPrefill(publisherToken, userToken);
    });

    useEffect(() => {
        if (prefillResult.state === 'not started') {
            const searchParams = new URLSearchParams(window.location.search);
            startPrefill(searchParams.get("publisher_token"));
        }
    });

    if (state === 'prefill') {
        // if not started, we're about to start
        if (prefillResult.state === "loading" || prefillResult.state === "not started") {
            return (
                <div class="pa_wrapper2">
                    <Loading class="pa_loading-prefill" text="Analyzing level..." />
                </div>
            )
        }
        if (prefillResult.state === "has error") {
            return (
                <div class="pa_wrapper2">
                    <div class="pa_loading-error">
                        <p><b>Error:</b>{prefillResult.message}</p>
                    </div>
                </div>
            )
        }
        return (
            <PublisherAddForm level={prefillResult.data}/>
        )
    }

    return <p>AAAAAAAAAA</p>
}

function PublisherAddCheckUser() {
    const user = useLoggedInUser();

    if (user.state === "loading") {
        return (
            <div class="pa_wrapper2">
                <Loading text="Checking user..." class="pa_loading-user" />
            </div>
        )
    }

    if (user.state === "has error") {
        return (
            <div class="pa_wrapper2">
                <p class="pa_loading-user-error">Please login to continue</p>
            </div>
        )
    }

    return <PublisherAddMainPhase />
}

export function PublisherAdd() {


    return (
        <div class="pa">
            <Header />
            <div class="pa_wrapper1">
                <PublisherAddCheckUser />
            </div>
        </div>
    )
}