import { useAtom } from 'jotai'
import { atomWithStorage } from 'jotai/utils'

export const authTokenAtom = atomWithStorage('authToken', "");

export const useAuthTokenAtom = useAtom(authTokenAtom);