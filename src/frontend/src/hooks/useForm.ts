import { useCallback, useEffect, useRef } from 'preact/hooks';
import { serialize } from '@shoelace-style/shoelace/dist/utilities/form.js';
import { safeParse, type BaseSchema } from 'valibot';

/**
 * @param schema - schema that the form data expects.
 * @param onFormSubmit - function to call with the form data on submit.
 * @returns - props for the form
 */
export function useForm<Payload>(schema: BaseSchema<unknown, Payload>, onFormSubmit: (p: Payload) => void) {
	const ref = useRef<HTMLFormElement>(null);

	const onSubmit = useCallback((event: SubmitEvent) => {
		// Executing in a timeout to let shoelace run first.
		// see https://shoelace.style/getting-started/form-controls
		event.preventDefault();
		if (ref.current === null) {
			return;
		}

		const data = serialize(ref.current);

		const result = safeParse(schema, data);
		if (result.success) {
			onFormSubmit(result.output);
		}

		console.warn('Form data did not match given guard, so not submitting.');
		console.warn(result.issues);
	}, [onFormSubmit]);

	// Mount after shoelace: https://next.shoelace.style/getting-started/form-controls
	useEffect(() => {
		if (ref.current) {
			ref.current.addEventListener('submit', onSubmit);
		}

		return () => {
			ref.current?.removeEventListener('submit', onSubmit);
		};
	}, [onSubmit]);

	return {
		ref,
	};
}
