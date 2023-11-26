import { client } from "./client";
import * as tg from "generic-type-guard";

export type User = {
    id: string;
    name: string;
    avatar_url: string | null;
    // we don't read cutoff atm
}

export const isUser : tg.TypeGuard<User> = tg.isLikeObject({
    id: tg.isString,
    name: tg.isString,
    avatar_url: tg.isNullable(tg.isString)
});

export async function getLoggedInUser(authToken: string) {
    return client.get("user/me", {
        guard: isUser,
        headers: {
            Authorization: `Bearer ${authToken}`
        }
    });
}

type OrchardTokenResponse = {
    token: string;
    expires_in: number;
}

const isOrchardTokenResponse: tg.TypeGuard<OrchardTokenResponse> = tg.isLikeObject({
    token: tg.isString,
    expires_in: tg.isNumber
});

export async function getOrchardTokenResponseFromDiscord(code: string) {
    return client.post("auth/token/discord", {
        guard: isOrchardTokenResponse,
        json: {
            code,
            redirect_uri: window.location.origin + window.location.pathname
        }
    });
}