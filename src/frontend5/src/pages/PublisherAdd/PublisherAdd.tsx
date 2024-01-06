import "./PublisherAdd.css";
import { Loading } from "@orchard/components/Loading";
import { Header } from "@orchard/components/Header";
import { addRDLevel, getRDLevelPrefill } from "@orchard/api/levels/levels";
import { useEffect } from "preact/hooks";
import { EditLevel } from "@orchard/components/EditLevel";
import { Publisher, getPublisher } from "@orchard/api/publisher";
import combinePromises from "@orchard/utils/combinePromises";
import { AddRDLevelPayload, RDPrefillResultWithToken } from "@orchard/api/levels/types";
import { useAsyncAction2 as useAsyncAction } from "@orchard/hooks/useAsync";

type PublisherAddFormProps = {
    prefillResult: RDPrefillResultWithToken
    publisher: Publisher
    publisherToken: string
}

function PublisherAddForm({prefillResult, publisher, publisherToken}: PublisherAddFormProps) {
    const { result, signed_token: signedToken } = prefillResult;

    const onSubmit = async (payload: AddRDLevelPayload) => {
        const result = await addRDLevel(signedToken, publisherToken, payload);
        console.log(result);
    }

    return (
        <div class="pa_form-wrapper">
            <EditLevel levelPrefill={result} publisher={publisher} class="pa_edit-level" onSubmit={onSubmit} />
        </div>
    )
}

function PublisherAddMainPhase() {    
    const [prefillResult, startPrefill] = useAsyncAction(async (publisherToken: string | null) => {
        if (publisherToken == null) {
            throw new Error("No publisher token given. Try the command again in discord")
        }
        return combinePromises({
            prefill: getRDLevelPrefill(publisherToken),
            publisher: getPublisher(publisherToken),
            publisherToken
        })
    });

    useEffect(() => {
        if (prefillResult.state === 'not started') {
            const searchParams = new URLSearchParams(window.location.search);
            startPrefill(searchParams.get("publisher_token"));
        }
    }, [prefillResult]);

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
    const {prefill, publisher, publisherToken} = prefillResult.data;

    return (
        <PublisherAddForm prefillResult={prefill} publisher={publisher} publisherToken={publisherToken}/>
    )
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