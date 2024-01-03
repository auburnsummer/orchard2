import { useCallback, useEffect, useRef } from "preact/hooks";

import * as tg from "generic-type-guard";
import { serialize } from '@shoelace-style/shoelace/dist/utilities/form.js';

/**
 * @param guard - type guard that the form data expects.
 * @param onFormSubmit - function to call with the form data on submit.
 * @returns - props for the form
 */
export function useForm<Payload>(guard: tg.TypeGuard<Payload>, onFormSubmit: (p: Payload) => void) {
    const ref = useRef<HTMLFormElement | null>(null);

    const onSubmit = useCallback((e: SubmitEvent) => {
        // executing in a timeout to let shoelace run first.
        // see https://shoelace.style/getting-started/form-controls
        e.preventDefault();
        if (ref.current == null) {
            return;
        }
        const data = serialize(ref.current);
        if (guard(data)) {
            onFormSubmit(data);
            return;
        }
        console.warn("Form data did not match given guard, so not submitting.")    
    }, [onFormSubmit]);

    // mount after shoelace: https://next.shoelace.style/getting-started/form-controls
    useEffect(() => {
        if (ref.current) {
            ref.current.addEventListener('submit', onSubmit);
        }
        return () => {
            ref.current?.removeEventListener('submit', onSubmit);
        }
    }, [onSubmit]);

    return {
        ref
    }
}