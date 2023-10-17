import { assertNever, getErrorMessage } from "@orchard/utils/error"
import { Getter, Setter, atom } from "jotai"
import { loadable } from "jotai/utils"

export type AsyncState<Result> = {
    state: "not started",
} | {
    state: "loading"
} | {
    state: "has error",
    error: unknown,
    message: string
} | {
    state: "has data",
    data: Awaited<Result>
}
export type AsyncReadState<Result> = Exclude<AsyncState<Result>, {state: "not started"}>;

export type ActionInputFunction<Args extends unknown[], Result> = (get: Getter, set: Setter, ...args: Args) => Promise<Result>

export function startableAction<Args extends unknown[], Result>(func: ActionInputFunction<Args, Result>) {
    const outputAtom = atom<AsyncState<Result>>({state: "not started"});
    return atom(
        get => get(outputAtom),
        (get, set, ...args: Args) => {
            (async (get, set, ...args) => {
                set(outputAtom, {state: "loading"});
                try {
                    const data = await func(get, set, ...args);
                    set(outputAtom, {state: "has data", data});
                } catch (err: unknown) {
                    const message = await getErrorMessage(err);
                    set(outputAtom, {state: "has error", error: err, message})
                }
            })(get, set, ...args);
        }
    )
}

export type ValueInputFunction<Result> = (get: Getter) => Promise<Result>

export function loadableValue<Result>(func: ValueInputFunction<Result>) {
    const loadableAtom = loadable(atom(
        async get => await func(get)
    ));

    const errorMessageAtom = loadable(atom(
        async get => {
            const result = get(loadableAtom);
            if (result.state === 'hasError') {
                const error_message = await getErrorMessage(result.error);
                return error_message;
            }
            return "";
        }
    ))

    const wrappedAtom = atom<AsyncReadState<Result>>(
        get => {
            const result = get(loadableAtom);
            if (result.state === 'loading') {
                return {
                    state: "loading"
                }
            }
            if (result.state === 'hasData') {
                return {
                    state: "has data",
                    data: result.data
                }
            }
            if (result.state === 'hasError') {
                const errorMessage = get(errorMessageAtom);
                if (errorMessage.state === 'loading') {
                    return {
                        state: "loading"
                    }
                }
                if (errorMessage.state === 'hasError') {
                    return {
                        state: "has error",
                        error: Error("getErrorMessage threw"),
                        message: "getErrorMessage should never throw! If you see this, ping auburn"
                    }
                }
                return {
                    state: "has error",
                    error: null,
                    message: errorMessage.data
                }
            }
            assertNever(result);
        }
    );

    return wrappedAtom;
}