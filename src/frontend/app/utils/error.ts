import * as tg from "generic-type-guard";
import { json } from "@remix-run/node";

export type OrchardError = {
    error_code: string
    message: string
}

export const isOrchardError : tg.TypeGuard<OrchardError> = tg.isLikeObject({
    error_code: tg.isString,
    message: tg.isString
})

export function bail(error: OrchardError, init?: number | ResponseInit | undefined): never {
    throw json(error, init);
}