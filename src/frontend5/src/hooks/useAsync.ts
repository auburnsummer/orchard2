import { getErrorMessage } from "@orchard/utils/error";
import { tuple } from "@orchard/utils/grabbag";
import { useMemo, useState } from "preact/hooks";

type AsyncActionFunction<Args extends unknown[], Result> = (...args: Args) => Promise<Result>;

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
};

/**
 * Hook to control the execution of an async function.
 * The first value is the state of the function.
 * The second value is a function to start the execution.
 * nb: The input function should be memoized to avoid rerenders.
 */
export function useAsyncAction2<Args extends unknown[], Result>(func: AsyncActionFunction<Args, Result>) {
    const [value, setValue] = useState<AsyncState<Result>>({state: "not started"});

    const runFunc = useMemo(() => {
        const runner = async (...args: Args) => {
            setValue({state: "loading"});
            try {
                await new Promise((resolve, reject) => setTimeout(resolve, 5000));
                const data = await func(...args);
                setValue({
                    state: "has data",
                    data
                });
            } catch (err) {
                const errorMessage = await getErrorMessage(err);
                setValue({
                    state: "has error",
                    message: errorMessage,
                    error: err
                });
            }
        };
        return (...args: Args) => void runner(...args);
    }, [func, setValue]);

    return tuple(value, runFunc)
}