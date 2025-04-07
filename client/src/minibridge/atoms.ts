import { Config } from "./config";
import { atom } from "jotai";
import { DjangoBridgeResponse, djangoGet, djangoPost, Message, RenderResponse } from "./fetch";

import { atomWithLocation } from "jotai-location";
import { makeCanonicalURL } from "./utils";

export const configAtom = atom<Config>();

export const initialResponseAtom = atom<DjangoBridgeResponse>();

export const currentRenderAtom = atom<RenderResponse>();

export const locationAtom = atomWithLocation();

export const isLoadingAtom = atom(false);

export const handleResponseAtom = atom(null, async (_get, set, response: DjangoBridgeResponse, url: URL) => {
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
        set(locationAtom, url);
    }
    else if (response.action === "redirect") {
        set(navigateAtom, makeCanonicalURL(response.path))
    }
});

export const messagesAtom = atom<Message[]>([]);

export const navigateAtom = atom(null, async (_get, set, url: URL) => {
    set(isLoadingAtom, true);
    const resp = await djangoGet(url.toString());
    set(handleResponseAtom, resp, url);
});

export const formSubmitAtom = atom(null, async (_get, set, url: URL, formData: FormData) => {
    set(isLoadingAtom, true);
    const resp = await djangoPost(url.toString(), formData);
    set(handleResponseAtom, resp, url);
})