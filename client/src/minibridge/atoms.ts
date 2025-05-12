import { Config } from "./config";
import { atom } from "jotai";
import { DjangoBridgeResponse, djangoGet, djangoPost, Message, RenderResponse } from "./fetch";

import { atomWithLocation } from "jotai-location";
import { makeCanonicalURL } from "./utils";

// stores the djangobridge Config. this doesn't change.
export const configAtom = atom<Config>();

// " " " initialResponse. this doesn't change.
export const initialResponseAtom = atom<DjangoBridgeResponse>();

// the response of the last "render" request from django -- this is what view we're showing
export const currentRenderAtom = atom<RenderResponse>();

export const locationAtom = atomWithLocation();

// primarily for showing loading bar
export const isLoadingAtom = atom(false);

// arbitrary id with the last running GET request.
// if this doesn't match by the time we handle the response, it means that
// another request was made in the meantime, and we should ignore this one.
// nb: this only applies to GET. we don't want the user to be able to cancel a 
// POST accidentally. 
const currentRequestIdAtom = atom(0);


export const handleResponseAtom = atom(
    null,
    async (get, set, response: DjangoBridgeResponse, url: URL, requestId?: number) => {
        if (requestId !== undefined) {
            if (requestId !== get(currentRequestIdAtom)) {
                console.warn(`Ignoring request with id ${requestId} as a more recent GET has been made`);
                return;
            }
        }
        if (response.action === "render") {
            set(isLoadingAtom, false);
            set(currentRenderAtom, response);
            set(messagesAtom, (prev) => [...prev, ...response.messages]);
            // only set the URL if it's changed
            // otherwise we will have multiple of the same URL in the stack
            if (url.toString() !== new URL(document.location.href).toString()) {
                set(locationAtom, url);
            }
        }
        else if (response.action === "reload") {
            // reload the page
            window.location.href = url.toString();
        }
        else if (response.action === "redirect") {
            set(navigateAtom, makeCanonicalURL(response.path))
        }
        else if (response.action === "network-error") {
            set(messagesAtom, (prev) => [...prev, {
                html: "A network error occurred",
                level: "error"
            }]);
        }
        else if (response.action === "server-error") {
            set(messagesAtom, (prev) => [...prev, {
                html: "A server error occurred",
                level: "error"
            }]);
        }
    }
);

export const messagesAtom = atom<Message[]>([]);

export const navigateAtom = atom(null, async (get, set, url: URL) => {
    const requestId = get(currentRequestIdAtom) + 1;
    set(currentRequestIdAtom, requestId);
    set(isLoadingAtom, true);
    const resp = await djangoGet(url.toString());
    set(handleResponseAtom, resp, url, requestId);
});

export const formSubmitAtom = atom(null, async (_get, set, url: URL, formData: FormData) => {
    set(isLoadingAtom, true);
    const resp = await djangoPost(url.toString(), formData);
    set(handleResponseAtom, resp, url);
})