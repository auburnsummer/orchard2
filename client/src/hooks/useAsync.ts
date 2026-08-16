import { useCallback, useState } from "react";

type asyncState<T> = {
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

type asyncResult<T> = [
    state: asyncState<T>,
    execute: () => void
];

export function useAsync<T>(
    func: () => Promise<T>
): asyncResult<T> {
    const [state, setState] = useState<asyncState<T>>({ status: "idle" });

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