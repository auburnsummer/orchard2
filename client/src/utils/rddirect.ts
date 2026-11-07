import { useMessages } from "@cafe/minibridge/hooks";
import { useCallback } from "react";
import { delayMilliseconds } from "./wait";
import { useUser } from "@cafe/hooks/useUser";
import isNetworkError from 'is-network-error';

export const CAFE_LINK_BASE_URL = "http://127.0.0.1:2615";

export const CAFE_LINK_STATUS_URL = `${CAFE_LINK_BASE_URL}/status`;

// how long to wait before we assume the server is not online, and we should launch RD then try again.
export const WAIT_TIME_MILLISECONDS = 2000;

// How long to wait after launching RD before attempting to play the level.
export const WAIT_TIME_AFTER_LAUNCH_MILLISECONDS = 5000;

// The number of times we will retry connecting to the server before giving up.
export const MAX_RETRY_ATTEMPTS = 20;

export const WAIT_TIME_BETWEEN_ATTEMPTS_MILLISECONDS = 2000;

// So in total, if you have to launch RD we think it will at most take 5 + (20 * 2) seconds = 45 seconds.
// if your computer takes longer than that... sorry :D

export function getCafeLinkPlayUrl(levelId: string, transient: boolean): string {
    // ex http://127.0.0.1:2615/play?uri=cafe://r62wZqQG&transient
    const transientFragment = transient ? "&transient" : "";
    return `${CAFE_LINK_BASE_URL}/play?uri=cafe://${levelId}${transientFragment}`;
}

export async function cafeLinkConnectionTest() {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), WAIT_TIME_MILLISECONDS);

    try {
        const response = await fetch(CAFE_LINK_STATUS_URL, { method: 'GET', signal: controller.signal });
        clearTimeout(timeoutId);

        if (!response.ok) {
            throw new Error(`HTTP error ${response.status}`);
        }
        const body = await response.json();
        if (body.status !== "ok") {
            return false;
        }
        return true;
    } catch (error) {
        clearTimeout(timeoutId);
        return false;
    }
}

export async function cafeLinkDirectPlay(levelId: string, transient: boolean) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), WAIT_TIME_MILLISECONDS);

    const playUrl = getCafeLinkPlayUrl(levelId, transient);
    const response = await fetch(playUrl, { method: 'POST', signal: controller.signal });
    clearTimeout(timeoutId);
    if (!response.ok) {
        throw new Error(`HTTP error ${response.status}`);
    }
}

export function useCafeLinkDirectPlay(levelId: string): (transient: boolean) => void {
    const user = useUser();

    const launchRdFunction = async () => {
        // rd_launch_url is usually not HTTP, so we can't use fetch here.
        const element = document.createElement("a");
        element.href = user.rd_launch_url;
        element.style.display = "none";
        document.body.appendChild(element);
        element.click();
        document.body.removeChild(element);
    }

    const [, setMessages] = useMessages();

    const errorToast = (error: Error) => {
        setMessages((messages) => [...messages, { level: "error", html: error.message }]);
    };

    const successToast = (message: string) => {
        setMessages((messages) => [...messages, { level: "success", html: message }]);
    }

    return useCallback(async (transient: boolean) => {
        try {
            // First attempt to get the level.
            await cafeLinkDirectPlay(levelId, transient);
            successToast(`Playing level!`);
        } catch (error) {
            if ((error instanceof Error && error.name === 'AbortError') || isNetworkError(error)) {
                // the server didn't respond in time. we'll launch RD and then ping for it to be online.
                try {
                    await launchRdFunction();
                } catch (error) {
                    errorToast(new Error(`Failed to launch RD`));
                    return;
                }
                await delayMilliseconds(WAIT_TIME_AFTER_LAUNCH_MILLISECONDS);
                // ping the server to check if it's online.
                let online = false;
                for (let attempt = 0; attempt < MAX_RETRY_ATTEMPTS; attempt++) {
                    try {
                        online = await cafeLinkConnectionTest();
                        if (online) break;
                    } catch (error) {
                        // Ignore errors and retry.
                    }
                    await delayMilliseconds(WAIT_TIME_BETWEEN_ATTEMPTS_MILLISECONDS);
                }
                if (online) {
                    // The server is online, we can attempt to play the level again.
                    try {
                        await cafeLinkDirectPlay(levelId, transient);
                        successToast(`Playing level!`);
                        return;
                    } catch (error) {
                        // somehow we failed even after the server came online??
                        errorToast(new Error(`Failed to play level`));
                        return;
                    }
                } else {
                    errorToast(new Error(`Failed to play level`));
                }
            }
            else if (error instanceof Error) {
                errorToast(error);
            }
        }
    }, [levelId, errorToast, successToast, launchRdFunction]);
}                                                                       