import { Config } from "./config";
import { DjangoBridgeResponse } from "./fetch";

import { useHydrateAtoms } from "jotai/utils";
import {
  configAtom,
  handleResponseAtom,
  initialResponseAtom,
  navigateAtom,
} from "./atoms";
import { ReactNode, useEffect } from "react";
import { useSetAtom } from "jotai";
import { ProviderStack } from "./components/ProviderStack";

interface AppProps {
  config: Config;
  initialResponse: DjangoBridgeResponse;
  children: ReactNode;
}

export function App({ config, initialResponse, children }: AppProps) {
  useHydrateAtoms([
    [configAtom, config],
    [initialResponseAtom, initialResponse],
  ]);
  const handleResponse = useSetAtom(handleResponseAtom);
  const navigate = useSetAtom(navigateAtom);

  // Remove loader animation
  useEffect(() => {
    const loadingScreen = document.querySelector(".django-bridge-load");
    if (loadingScreen instanceof HTMLElement) {
      loadingScreen.remove();
    }
  }, []);

  // Process initial response
  useEffect(() => {
    void handleResponse(initialResponse, new URL(window.location.href));
  }, []);

  // Listen to popstate (user hitting back/forward in browser)
  useEffect(() => {
    const popStateHandler = () => {
      navigate(new URL(window.location.href));
    };
    window.addEventListener("popstate", popStateHandler);
    return () => {
      window.removeEventListener("popstate", popStateHandler);
    };
  }, []);

  return <ProviderStack>{children}</ProviderStack>;
}
