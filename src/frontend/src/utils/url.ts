
// eslint-disable-next-line @typescript-eslint/ban-types
type AllowedValues = string | string[] | number | number[] | boolean | boolean[] | null | undefined;

export function serializeObjectToSearchParams(object: Record<string, AllowedValues>) {
	const freshSearchParams = new URLSearchParams();
	for (const [key, value] of Object.entries(object)) {
		if (value === null || value === undefined) {
			continue;
		}

		if (Array.isArray(value)) {
			for (const v of value) {
				freshSearchParams.append(key, `${v}`);
			}
		} else {
			freshSearchParams.append(key, `${value}`);
		}
	}

	return freshSearchParams;
}
