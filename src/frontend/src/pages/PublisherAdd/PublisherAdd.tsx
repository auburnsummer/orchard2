import { authTokenAtom } from "@orchard/stores/auth";
import "./PublisherAdd.css";
import { Loading } from "@orchard/components/Loading";
import { Header } from "@orchard/components/Header";
import { atom, useAtom } from "jotai";
import { useAsyncAction } from "@orchard/hooks/useAsync";
import { RDPrefillResult, getRDLevelPrefill } from "@orchard/api/levels/levels";
import { useEffect, useRef } from "preact/hooks";
import { atomWithReset } from "jotai/utils";
import { EditLevel } from "@orchard/components/EditLevel";
import { Publisher, getPublisher } from "@orchard/api/publisher";
import combinePromises from "@orchard/utils/combinePromises";

type STATES = "prefill"

const stateAtom = atom<STATES>("prefill");

type PublisherAddFormProps = {
    level: RDPrefillResult;
    publisher: Publisher
}

function PublisherAddForm({level, publisher}: PublisherAddFormProps) {
    const levelAtom = useRef(atomWithReset(level));

    const [levelPrefill, setLevelPrefill] = useAtom(levelAtom.current);

    return (
        <div class="pa_form-wrapper">
            <EditLevel levelPrefill={levelPrefill} publisher={publisher} class="pa_edit-level" />
        </div>
    )
}

function PublisherAddMainPhase() {
    const [state, setState] = useAtom(stateAtom);
    
    const [prefillResult, startPrefill] = useAsyncAction(async (get, _set, publisherToken: string | null) => {
        if (publisherToken == null) {
            throw new Error("No publisher token given. Try the command again in discord")
        }
        return combinePromises({
            prefill: getRDLevelPrefill(publisherToken),
            publisher: getPublisher(publisherToken)
        })
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
        const {prefill, publisher} = prefillResult.data;
        return (
            <PublisherAddForm level={prefill.result} publisher={publisher}/>
        )
    }

    return <p>AAAAAAAAAA</p>
}


export function PublisherAdd() {
    return (
        <div class="pa">
            <Header class="pa_header" />
            <div class="pa_wrapper1">
                <PublisherAddMainPhase />
            </div>
        </div>
    )
}