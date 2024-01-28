import { HTTPError } from 'ky';
import { object, string, type Output, safeParse } from 'valibot';

const orchardErrorSchema = object({
	/* eslint-disable @typescript-eslint/naming-convention */
	error_code: string(),
	message: string(),
	/* eslint-enable @typescript-eslint/naming-convention */
});

// All my backend code uses this error schema.
export type OrchardError = Output<typeof orchardErrorSchema>;

/**
 * Given "something" that's been thrown, try to get a decent error message out of it.
 * This isn't particularly smart atm, if it's one of my errors it will return a nice message and
 * otherwise just get the "message" property if it exists.
 */
export async function getErrorMessage(value: unknown) {
	// Anything can be thrown, if it's not an Error, we won't try to deal with it any further.
	if (!(value instanceof Error)) {
		// But we'll log it I guess
		console.error(value);
		return 'Undefined Error';
	}

	if (value instanceof HTTPError) {
		try {
			const resp = await value.response.json() as unknown;
			const result = safeParse(orchardErrorSchema, resp);
			if (result.success) {
				const { output } = result;
				return `${output.error_code}: ${output.message}`;
			}
			// Nothing
		} catch {
			// Nothing
		}
	}

	return value.message;
}

/**
 * Always throws an error.
 * For TypeScript reasons to tell it that a codepath is never reachable.
 * https://stackoverflow.com/a/74605768
 */
export function assertNever(_x: never): never {
	throw new Error('Assert never');
}

