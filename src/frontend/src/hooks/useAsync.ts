import { ActionInputFunction, ValueInputFunction, loadableValue, startableAction } from "@orchard/stores/async"
import { useAtom, useAtomValue } from "jotai"
import { useRef } from "preact/hooks"

export function useLoadableValue<Result>(func: ValueInputFunction<Result>) {
    const anAtom = useRef(loadableValue(func));
    return useAtomValue(anAtom.current);
}

/**
 * Hook to control the execution of an async function.
 * The first value is the state of the function.
 * The second value is a function to start the execution.
 */
export function useAsyncAction<Args extends unknown[], Result>(func: ActionInputFunction<Args, Result>) {
    const myCoolAtom = useRef(startableAction(func));
    return useAtom(myCoolAtom.current);
}