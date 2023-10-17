import { useEffect } from "preact/hooks";

export function useLog(value: unknown) {
    useEffect(() => {
        console.log(value);
    }, [value]);
}