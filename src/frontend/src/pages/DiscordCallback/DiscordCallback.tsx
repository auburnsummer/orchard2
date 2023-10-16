import { Suspense } from "preact/compat";
import "./DiscordCallback.css";
import { atom, useAtom, useAtomValue } from "jotai";
import ky from "ky";
import { useEffect, useErrorBoundary } from "preact/hooks";
import { ComponentChildren } from "preact";
import { Icon, Spinner } from "@orchard/ui";
import { getErrorMessage } from "@orchard/utils/error";
import { loadable } from "jotai/utils";
import * as tg from "generic-type-guard";
import { useAuthToken } from "@orchard/stores/auth";

type OrchardTokenResponse = {
    token: string;
    expires_in: number;
}

const isOrchardTokenResponse: tg.TypeGuard<OrchardTokenResponse> = tg.isLikeObject({
    token: tg.isString,
    expires_in: tg.isNumber
});

const orchardTokenAtom = atom(async () => {
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get("code");
    if (!code) {
        throw new Error("Expected a code query parameter.");
    }
    const resp = await ky.post("auth/token/discord", {
        prefixUrl: import.meta.env.VITE_API_URL,
        json: {
            code,
            redirect_uri: window.location.origin + window.location.pathname
        }
    });
    const data = await resp.json();
    if (isOrchardTokenResponse(data)) {
        return data;
    }
    throw new Error(`Response did not match schema: ${JSON.stringify(data)}`);
});

type ErrorBoundaryProps = {
    children: ComponentChildren;
}

// set to error in ErrorBoundary if an error has occurred.
const errorBoundaryAtom = atom<unknown>(undefined);
// reads the errorBoundaryAtom and makes a message out of it.
const errorMessageAtom = loadable(atom(async (get) => getErrorMessage(get(errorBoundaryAtom))));

function ErrorBoundary({children}: ErrorBoundaryProps) {
    const [error] = useErrorBoundary();
    const [_, setErrorB] = useAtom(errorBoundaryAtom);
    useEffect(() => {
        setErrorB(error);
    }, [error]);

    const message = useAtomValue(errorMessageAtom);
    
    if (error == undefined) {
        // error is undefined if there is no error, all good, pass through children.
        return <>{children}</>
    }

    if (message.state === 'loading') {
        // realistically errorMessageAtom only has to parse json. it's only
        // "technically" async but we expect it to resolve basically instantly.
        return (
            <></>
        )
    }
    if (message.state === 'hasError') {
        // getErrorMessage should never throw. if it does, uhh I've definitely screwed up somewhere.
        return (
            <p>Error occured parsing error. If you see this, I've made a mistake! please ping auburn now. {JSON.stringify(message.error)} {message.error}</p>
        )
    }

    return (
        <div class="dc_error">
            <Icon class="dc_error-icon" name="exclamation-triangle" />
            <span class="dc_error-text"><b>Error:</b> {message.data}</span>
            <span class="dc_error-advice">Please try closing this tab and logging in again. If this error persists, ping Auburn, thanks!</span>
        </div>
    )
}

function DiscordCallbackContent() {
    const token = useAtomValue(orchardTokenAtom);
    const [_, setAuthToken] = useAuthToken();

    useEffect(() => {
        setAuthToken(token.token);
        setTimeout(window.close, 500);
    }, [token]);

    return (
        <div class="dc_success">
            <Icon class="dc_success-icon" name="check-circle" />
            <span class="dc_success-text">Log in successful! This page will close automatically.</span>
        </div>
    )
}

function DiscordCallbackLoading() {
    return (
        <div class="dc_loading">
            <Spinner class="dc_loading-spinner" />
            <span class="dc_loading-text">Logging in...</span>
        </div>
    )
}

export function DiscordCallback() {
    return (
        <div class="dc">
            <ErrorBoundary>
                <Suspense fallback={<DiscordCallbackLoading />}>
                    <DiscordCallbackContent />
                </Suspense>
            </ErrorBoundary>
        </div>
    )
}