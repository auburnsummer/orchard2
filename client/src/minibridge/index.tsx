import { Config } from "./config";
import { DjangoBridgeResponse } from "./fetch";

import { useHydrateAtoms } from "jotai/utils";
import { configAtom, handleResponseAtom, initialResponseAtom } from "./atoms";
import { ReactNode, useEffect } from "react";
import { useSetAtom } from "jotai";
import { ProviderStack } from "./components/ProviderStack";

interface AppProps {
    config: Config;
    initialResponse: DjangoBridgeResponse;
    children: ReactNode;
}

export function App({config, initialResponse, children}: AppProps) {
    useHydrateAtoms([
        [configAtom, config],
        [initialResponseAtom, initialResponse]
    ]);
    const handleResponse = useSetAtom(handleResponseAtom);

    useEffect(() => {
        const loadingScreen = document.querySelector(".django-bridge-load");
        if (loadingScreen instanceof HTMLElement) {
          loadingScreen.classList.add("django-bridge-load--hidden");
          setTimeout(() => {
            loadingScreen.remove();
          }, 200);
        }    
    }, []);

    useEffect(() => {
        void handleResponse(initialResponse);
    }, []);

    return (
        <ProviderStack>
            {children}
        </ProviderStack>
    );
}