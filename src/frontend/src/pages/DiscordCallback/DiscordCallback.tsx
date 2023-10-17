import "./DiscordCallback.css";
import ky from "ky";
import { Icon, Spinner } from "@orchard/ui";
import * as tg from "generic-type-guard";
import { useSetAtom } from "jotai";
import { useEffect } from "preact/hooks";
import { authTokenAtom } from "@orchard/stores/auth";
import { assertNever } from "@orchard/utils/error";
import { useAsyncAction } from "@orchard/hooks/useAsync";

type OrchardTokenResponse = {
    token: string;
    expires_in: number;
}

const isOrchardTokenResponse: tg.TypeGuard<OrchardTokenResponse> = tg.isLikeObject({
    token: tg.isString,
    expires_in: tg.isNumber
});

function DiscordCallbackContents() {
    const [output, startLoginAttempt] = useAsyncAction(async (_get, _set, code: string | null) => {
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
        throw new Error(`Response from auth/token/discord did not match schema: ${JSON.stringify(data)}`);
    })
    const setAuthToken = useSetAtom(authTokenAtom);

    useEffect(() => {
        if (output.state === 'not started') {
            const urlParams = new URLSearchParams(window.location.search);
            const code = urlParams.get("code"); 
            startLoginAttempt(code);
        }
        if (output.state === 'has data') {
            setAuthToken(output.data.token);
            setTimeout(window.close, 500);
        }
    }, [output]);

    if (output.state === 'not started' || output.state === 'loading') {
        return (
            <div class="dc_loading">
                <Spinner class="dc_loading-spinner" />
                <span class="dc_loading-text">Logging in...</span>
            </div>
        )
    }

    if (output.state === 'has error') {
        return (
            <div class="dc_error">
                <Icon class="dc_error-icon" name="exclamation-triangle" />
                <span class="dc_error-text"><b>Error:</b> {output.message}</span>
                <span class="dc_error-advice">Please try closing this window and logging in again. If this error persists, ping Auburn, thanks!</span>
            </div>
        )
    }

    if (output.state === 'has data') {
        return (
            <div class="dc_success">
                <Icon class="dc_success-icon" name="check-circle" />
                <span class="dc_success-text">Log in successful! This page will close automatically.</span>
            </div>
        )
    }

    assertNever(output);
}

export function DiscordCallback() {
    return (
        <div class="dc">
            <DiscordCallbackContents />
        </div>
    )
}
