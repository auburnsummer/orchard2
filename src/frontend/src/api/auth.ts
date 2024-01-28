import { nullish, object, string, number, type Output } from 'valibot';
import { client } from './client';

export const userSchema = object({
	id: string(),
	name: string(),
	avatar_url: nullish(string()),
});

export type User = Output<typeof userSchema>;

export async function getLoggedInUser(authToken: string) {
	return client.get('user/me', {
		schema: userSchema,
		headers: {
			Authorization: `Bearer ${authToken}`,
		},
	});
}

const orchardTokenResponseSchema = object({
	token: string(),
	expires_in: number(),
});

export async function getOrchardTokenResponseFromDiscord(code: string) {
	return client.post('auth/token/discord', {
		schema: orchardTokenResponseSchema,
		json: {
			code,
			redirect_uri: window.location.origin + window.location.pathname
		},
	});
}
