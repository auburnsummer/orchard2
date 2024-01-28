import ky from 'ky';
import { safeParse, type BaseSchema } from 'valibot';
import { getEnv } from '~/utils/env';

const prefixUrl = getEnv('VITE_API_URL');

const base = ky.extend({ prefixUrl, timeout: false });

type Input = Parameters<typeof ky>[0];
type KyOptions = NonNullable<Parameters<typeof ky>[1]>;

type Options<T> = KyOptions & {
	schema: BaseSchema<unknown, T>;
};

export const guardedRequest = (method: string) => async <T>(url: Input, options: Options<T>): Promise<T> => {
	const { schema, ...rest } = options;
	const resp = await base(url, {
		...rest,
		method,
	});
	const data = await resp.json();
	const parseResult = safeParse(schema, data);
	if (parseResult.success) {
		return parseResult.output;
	}

	// If we're here then the request was successful but the output did not match
	// the schema.
	const failedUrl = typeof url === 'string'
		? url
		: (url instanceof URL
			? url.href
			: url.url);

	const issues = parseResult.issues.map(i => i.message).join(', ');
	console.error(issues);
	throw new Error(`Response from ${failedUrl} did not match schema, ${issues}, see console for full trace. This is a bug, ping auburn!`);
};

export const client = {
	get: guardedRequest('get'),
	post: guardedRequest('post'),
	put: guardedRequest('put'),
	delete: guardedRequest('delete'),
	patch: guardedRequest('patch'),
	options: guardedRequest('options'),
	head: guardedRequest('head'),
};
