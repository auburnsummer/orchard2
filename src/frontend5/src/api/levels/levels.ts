import { client } from "../client.ts";

import { AddRDLevelPayload, RDSearchParams, isAddRDLevelResponse, isRDPrefillResultWithToken, isRDQueryResult } from "./types.ts";

// the url for the prefill is encoded in the token and cannot be changed by the user.
export async function getRDLevelPrefill(publisherToken: string) {
    return client.post("rdlevel/prefill", {
        guard: isRDPrefillResultWithToken,
        headers: {
            authorization: `Bearer ${publisherToken}`
        }
    })
}



export async function addRDLevel(prefillSignedToken: string, publisherToken: string, payload: AddRDLevelPayload) {
    return client.post("rdlevel", {
        guard: isAddRDLevelResponse,
        json: {
            level: payload
        },
        headers: {
            Authorization: `Bearer ${prefillSignedToken},Bearer ${publisherToken}`
        }
    });
}


export async function search(params: RDSearchParams) {
    const searchParams = new URLSearchParams();
    Object.entries(params).forEach(([key, value]) => {
        if (!value) {
            return;
        }
        if (Array.isArray(value)) {
            value.forEach(v => searchParams.append(key, `${v}`))
        } else {
            searchParams.append(key, `${value}`)
        }
    })
    return client.get("rdlevel", {
        guard: isRDQueryResult,
        searchParams
    })
}