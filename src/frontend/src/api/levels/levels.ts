import { serializeObjectToSearchParams } from '~/utils/url';
import { client } from '../client';
import { type AddRDLevelPayload, rdPrefillResultWithTokenSchema, rdlevelResponseSchema, RDSearchParams, rdQueryResultSchema } from './schemas';

export async function getRDLevelPrefill(publisherToken: string) {
	return client.post('rdlevel/prefill', {
		schema: rdPrefillResultWithTokenSchema,
		headers: {
			authorization: `Bearer ${publisherToken}`,
		},
	});
}

export async function addRDLevel(prefillSignedToken: string, publisherToken: string, payload: AddRDLevelPayload) {
	return client.post('rdlevel', {
		schema: rdlevelResponseSchema,
		json: {
			level: payload,
		},
		headers: {
			Authorization: `Bearer ${prefillSignedToken},Bearer ${publisherToken}`,
		},
	});
}

export async function searchRDLevels(params: RDSearchParams) {
	return client.get('rdlevel', {
		schema: rdQueryResultSchema,
		searchParams: serializeObjectToSearchParams(params),
	});
}
