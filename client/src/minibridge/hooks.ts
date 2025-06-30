import { useAtom, useAtomValue, useSetAtom } from "jotai";
import { isLoadingAtom, locationAtom, messagesAtom, navigateAtom } from "./atoms";
import { useCallback } from "react";
import { makeCanonicalURL } from "./utils";

// copied from useSetAtom.d.mts
type SetAtom<Args extends unknown[], Result> = (...args: Args) => Result;
type ExtractSetAtom<A> = A extends SetAtom<infer Args, infer Result> ? (...args: Args) => Result : never;

export const useIsLoading = () => useAtomValue(isLoadingAtom);

export const useMessages = () => useAtom(messagesAtom);

const useNavigate = () => {
    const a = useSetAtom(navigateAtom);
    const navigate = a as ExtractSetAtom<typeof a>;
    return navigate;
};

export const useLocation = () => {
    const navigate = useNavigate();
    const location = useAtomValue(locationAtom);
    return [location, navigate] as const;
}

export const useSearchParams = () => {
    const [location, navigate] = useLocation();
    const searchParams = location.searchParams || new URLSearchParams();
    const navigateViaSearchParams = useCallback((func: (params: URLSearchParams) => void | URLSearchParams) => {
        // either it returns a new searchParams or mutated the one we gave it
        const result = func(searchParams);
        const searchParamsToUse = result || searchParams;
        navigate(makeCanonicalURL(`${location.pathname}?${searchParamsToUse.toString()}`));
    }, [searchParams]);
    return [searchParams, navigateViaSearchParams] as const;
}