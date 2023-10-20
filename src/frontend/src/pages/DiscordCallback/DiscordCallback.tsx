import "./DiscordCallback.css";
import { Icon, Spinner } from "@orchard/ui";
import { useSetAtom } from "jotai";
import { useEffect } from "preact/hooks";
import { authTokenAtom } from "@orchard/stores/auth";
import { assertNever } from "@orchard/utils/error";
import { useAsyncAction } from "@orchard/hooks/useAsync";
import { getOrchardTokenResponseFromDiscord } from "@orchard/api/auth";
import { Loading } from "@orchard/components/Loading";

function DiscordCallbackContents() {
    const [output, startLoginAttempt] = useAsyncAction(async (_get, _set, code: string | null) => {
        if (!code) {
            throw new Error("Expected a code query parameter.");
        }
        return getOrchardTokenResponseFromDiscord(code);
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
            <Loading class="dc_loading" text="Logging in..."/>
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
