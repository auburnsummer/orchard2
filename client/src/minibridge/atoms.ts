import { Config } from "./config";
import { atom } from "jotai";
import { DjangoBridgeResponse, RenderResponse } from "./fetch";

export const configAtom = atom<Config>();

export const initialResponseAtom = atom<DjangoBridgeResponse>();

export const currentRenderAtom = atom<RenderResponse>();

export const handleResponseAtom = atom(null, async (_get, set, response: DjangoBridgeResponse) => {
    if (response.action === "render") {
        set(currentRenderAtom, response);
    }
})