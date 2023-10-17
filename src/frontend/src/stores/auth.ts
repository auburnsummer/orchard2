import { useAtom, useAtomValue, useSetAtom } from 'jotai'
import { atomWithStorage } from 'jotai/utils'
import ky from 'ky';
import * as tg from "generic-type-guard";
import { loadableValue } from './async';

export const authTokenAtom = atomWithStorage('authToken', "");

export const useAuthToken = () => useAtom(authTokenAtom);

export const useLogOut = () => {
    const setAuthToken = useSetAtom(authTokenAtom);
    return () => {
        setAuthToken("");
    }
}

export type User = {
    id: string;
    name: string;
    avatar_url?: string;
    // we don't read cutoff atm
}

export const isUser : tg.TypeGuard<User> = tg.isLikeObject({
    id: tg.isString,
    name: tg.isString,
    avatar_url: tg.isOptional(tg.isString)
});


export const loggedInUserAtom = loadableValue(async (get) => {
    const token = get(authTokenAtom);
    if (token === "") {
        return undefined;
    }

    const resp = await ky.get("user/me", {
        prefixUrl: import.meta.env.VITE_API_URL,
        headers: {
            authorization: `Bearer ${token}`
        }
    });
    const data = await resp.json();
    if (!isUser(data)) {
        throw new Error(`Response from /user/me did not match schema: ${JSON.stringify(data)}`);
    }
    return data;
});

export const useLoggedInUser = () => useAtomValue(loggedInUserAtom);