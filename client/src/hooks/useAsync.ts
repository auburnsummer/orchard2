import { useCallback, useState } from "react";

export type AsyncState<T> = {
    status: "idle";
} | {
    status: "pending";
} | {
    status: "success";
    data: T;
} | {
    status: "error";
    error: Error;
}
    
export type AsyncResult<T> = [
    state: AsyncState<T>,
    execute: () => void
];

export function useAsync<T>(
    func: () => Promise<T>
): AsyncResult<T> {
    const [state, setState] = useState<AsyncState<T>>({ status: "idle" });

    const execute = useCallback(() => {
        setState({ status: "pending" });
        func()
            .then((data) => {
                setState({ status: "success", data });
            })
            .catch((error) => {
                if (!(error instanceof Error)) {
                    error = new Error("Unknown error");
                }
                setState({ status: "error", error });
            });
    }, [func]);

    return [state, execute];
}