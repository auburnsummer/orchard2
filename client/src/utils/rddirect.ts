import { useMessages } from "@cafe/minibridge/hooks";
import { useCallback } from "react";

export const CAFE_LINK_BASE_URL = "http://127.0.0.1:2615";

export const CAFE_LINK_STATUS_URL = `${CAFE_LINK_BASE_URL}/status`;

export function getCafeLinkPlayUrl(levelId: string, transient: boolean): string {
    // ex http://127.0.0.1:2615/play?uri=cafe://r62wZqQG&transient
    const transientFragment = transient ? "&transient" : "";
    return `${CAFE_LINK_BASE_URL}/play?uri=cafe://${levelId}${transientFragment}`;
}

export function useCafeLinkDirectPlay(levelId: string): (transient: boolean) => void {
    const [, setMessages] = useMessages();

    const errorToast = (error: Error) => {
        setMessages((messages) => [...messages, { level: "error", html: error.message }]);
    };

    const successToast = (message: string) => {
        setMessages((messages) => [...messages, { level: "success", html: message }]);
    }

    return useCallback((transient: boolean) => {
        const playUrl = getCafeLinkPlayUrl(levelId, transient);
        fetch(playUrl, { method: 'POST' })
            .then((response) => {
                if (!response.ok) {
                    errorToast(new Error(`HTTP error ${response.status}`));
                } else {
                    successToast(`Playing level!`);
                }
            })
            .catch((error) => {
                errorToast(error);
            });
    }, [levelId]);
}