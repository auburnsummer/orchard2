import { useAtomValue } from "jotai";
import { ReactNode } from "react";
import { currentRenderAtom, configAtom } from "../atoms";

type ProviderStackProps = {
  children: ReactNode;
};

export function ProviderStack({ children }: ProviderStackProps) {
  const currentRender = useAtomValue(currentRenderAtom);
  const config = useAtomValue(configAtom);
  if (!currentRender || !config) {
    return <></>;
  }

  return Object.keys(config.contextProviders).reduce((prev, key) => {
    // this is always defined because we're iterating on Object.keys of the thing
    const provider = config.contextProviders[key]!;
    return (
      <provider.Provider value={currentRender.context[key]}>
        {prev}
      </provider.Provider>
    );
  }, children);
}
