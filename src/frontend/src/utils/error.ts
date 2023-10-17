import { HTTPError } from "ky";
import * as tg from "generic-type-guard";

// all my backend code uses this error schema.
export type OrchardError = {
    error_code: string;
    message: string;
}

export const isOrchardError: tg.TypeGuard<OrchardError> = tg.isLikeObject({
    error_code: tg.isString,
    message: tg.isString
});



/**
 * Given "something" that's been thrown, try to get a decent error message out of it.
 */
export async function getErrorMessage(val: unknown) {
    // anything can be thrown, if it's not an Error, we won't try to deal with it any further.
    if (!(val instanceof Error)) {
        return "Undefined error";
    }
    if (val instanceof HTTPError) {
        try {
            const resp = await val.response.json();
            if (isOrchardError(resp)) {
                return `${resp.error_code}: ${resp.message}`;
            }
        }
        catch {
            // nothing
        }
    }
    return val.message;
}

/**
 * Always throws an error.
 * For TypeScript reasons: https://stackoverflow.com/a/74605768
 */
export function assertNever(x: never): never {
    throw new Error("Unexpected Value: " + x);
  }
  