import { Config } from "./config";
import { atom } from "jotai";
import { DjangoBridgeResponse, djangoGet, RenderResponse } from "./fetch";

import { atomWithLocation } from "jotai-location";

export const configAtom = atom<Config>();

export const initialResponseAtom = atom<DjangoBridgeResponse>();

export const currentRenderAtom = atom<RenderResponse>();

export const handleResponseAtom = atom(null, async (_get, set, response: DjangoBridgeResponse) => {
    if (response.action === "render") {
        set(currentRenderAtom, response);
    }
})

export const locationAtom = atomWithLocation();

export const navigateAtom = atom(null, async (get, set, url: URL) => {
    const location = get(locationAtom);
    async function runner() {
        const resp = await djangoGet(url.toString());
        if (resp.action === "render") {
            set(locationAtom, url);
            set(currentRenderAtom, resp);
        }
    }
    void runner();
});