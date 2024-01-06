import { useAtom, useAtomValue, useSetAtom } from 'jotai'
import { atomWithStorage } from 'jotai/utils'
import { loadableValue } from './async';
import { getLoggedInUser } from '@orchard/api/auth';

export const authTokenAtom = atomWithStorage('authToken', "");

export const useAuthToken = () => useAtom(authTokenAtom);

export const useLogOut = () => {
    const setAuthToken = useSetAtom(authTokenAtom);
    return () => {
        setAuthToken("");
    }
}

export const loggedInUserAtom = loadableValue(async (get) => {
    const token = get(authTokenAtom);
    if (token === "") {
        throw new Error("No token, so the user is not logged in")
    }
    return await getLoggedInUser(token);
});

export const useLoggedInUser = () => useAtomValue(loggedInUserAtom);