import { useContext, createContext } from "react";

// We could get _anything_ from the server, but...
export type Flags = {
    [flagName: string]: boolean;
};

export const FlagContext = createContext<Flags>({});

// ...these will be the only allowable flag names.
type FlagName = "TestFlag" | "RDDirect";

export function useFlag(flagName: FlagName): boolean {
    const flags = useContext(FlagContext);
    if (!flags) {
        throw new Error("FlagContext not found");
    }
    if (!(flagName in flags)) {
        console.warn(`Flag ${flagName} not found, defaulting to false`);
        return false;
    }
    return flags[flagName] || false;
}