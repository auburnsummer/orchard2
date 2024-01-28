import { type Output, object, string } from 'valibot';
import { client } from './client';

export const publisherSchema = object({
	id: string(),
	name: string(),
});

export type Publisher = Output<typeof publisherSchema>;

export async function createNewDiscordPublisher(name: string, guildToken: string) {
	return client.post('publisher/new/discord', {
		schema: publisherSchema,
		headers: {
			Authorization: `Bearer ${guildToken}`,
		},
		json: {
			publisher_name: name,
		},
	});
}

export async function getPublisher(publisherToken: string) {
	return client.get('publisher/identify', {
		schema: publisherSchema,
		headers: {
			Authorization: `Bearer ${publisherToken}`,
		},
	});
}
