import { bail, isOrchardError } from "./error";

export const wrappedFetch = async (...args: Parameters<typeof fetch>) => {
    const result = await fetch(...args);
    if (!result.ok) {
        console.log("here1")
        try {
            const json = await result.json();
            if (isOrchardError(json)) {
                console.log("here");
                bail(json);
            }
        }
        catch (error) {
            // fall through to bottom case
        }
        throw result;
    }
    return result;
}