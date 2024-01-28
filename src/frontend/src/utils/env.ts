
export function getEnv(name: string) {
	const valueAny = import.meta.env[name] as unknown;
	if (typeof valueAny === 'string') {
		return valueAny;
	}

	throw new Error(`Environment variable ${name} not found.`);
}
