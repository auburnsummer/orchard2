import { array, object, string, boolean, number, type Output, merge, nullish } from 'valibot';
import { userSchema } from '../auth';
import { publisherSchema } from '../publisher';

/**
 * Corresponds to VitalsLevelBaseMutable in libs/vitals/msgspec_schema.py
 */
export const vitalsLevelBaseMutableSchema = object({
	artist: string(),
	artist_tokens: array(string()),
	song: string(),
	seizure_warning: boolean(),
	description: string(),
	hue: number(),
	authors: array(string()),
	authors_raw: string(),
	max_bpm: number(),
	min_bpm: number(),
	difficulty: number(),
	single_player: boolean(),
	two_player: boolean(),
	last_updated: string(),
	tags: array(string()),
	has_classics: boolean(),
	has_oneshots: boolean(),
	has_squareshots: boolean(),
	has_freezeshots: boolean(),
	has_freetimes: boolean(),
	has_holds: boolean(),
	has_skipshots: boolean(),
	has_window_dance: boolean(),
});

export type VitalsLevelBaseMutable = Output<typeof vitalsLevelBaseMutableSchema>;

/**
 * Corresponds to VitalsLevelBase in libs/vitals/msgspec_schema.py
 */
export const vitalsLevelBaseSchema = object({
	...vitalsLevelBaseMutableSchema.entries,
	sha1: string(),
	rdlevel_sha1: string(),
	is_animated: boolean(),
});

export type VitalsLevelBase = Output<typeof vitalsLevelBaseSchema>;

/**
 * Corresponds to RDPrefillResult in v1/models/rd_levels.py
 */
export const rdPrefillResultSchema = object({
	...vitalsLevelBaseSchema.entries,
	image: string(),
	thumb: string(),
	url: string(),
	icon: nullish(string()),
});

export type RDPrefillResult = Output<typeof rdPrefillResultSchema>;

/**
 * Corresponds to RDPrefillResultWithToken in v1/models/rd_levels.py
 */
export const rdPrefillResultWithTokenSchema = object({
	result: rdPrefillResultSchema,
	signed_token: string(),
});

export type RDPrefillResultWithToken = Output<typeof rdPrefillResultWithTokenSchema>;

/**
 * Corresponds to AddRDLevelPayload in v1/routes/rd_levels.py
 */
export const addRDLevelPayloadSchema = object({
	song_alt: string(),
});

export type AddRDLevelPayload = Output<typeof addRDLevelPayloadSchema>;

/**
 * Corresponds to RDLevel in v1/models/rd_levels.py
 */
export const rdLevelSchema = object({
	...rdPrefillResultSchema.entries,
	...addRDLevelPayloadSchema.entries,
	id: string(),
	uploader: userSchema,
	publisher: publisherSchema,
	uploaded: string(),
	approval: number(),
});

export type RDLevel = Output<typeof rdLevelSchema>;

/**
 * Corresponds to AddRDLevelResponse in v1/routes/rd_levels.py
 */
export const rdlevelResponseSchema = object({
	level: rdLevelSchema,
});

export type RDLevelResponse = Output<typeof rdlevelResponseSchema>;

/**
 * Corresponds to RDSearchParams in v1/models/rd_levels.py
 */
export const rdSearchParamsSchema = object({
	q: nullish(string()),
	tags: nullish(array(string())),
	artists: nullish(array(string())),
	authors: nullish(array(string())),
	min_bpm: nullish(number()),
	max_bpm: nullish(number()),
	difficulty: nullish(array(number())),
	single_player: nullish(boolean()),
	two_player: nullish(boolean()),
	has_classics: nullish(boolean()),
	has_oneshots: nullish(boolean()),
	has_squareshots: nullish(boolean()),
	has_freezeshots: nullish(boolean()),
	has_freetimes: nullish(boolean()),
	has_holds: nullish(boolean()),
	has_skipshots: nullish(boolean()),
	has_window_dance: nullish(boolean()),
	uploader: nullish(string()),
	publisher: nullish(string()),
	min_approval: nullish(number()),
	max_approval: nullish(number()),
	offset: nullish(number()),
	limit: nullish(number()),
});

export type RDSearchParams = Output<typeof rdSearchParamsSchema>;

/**
 * Corresponds to StrFacetValue in v1/models/rd_levels.py
 */
export const stringFacetValueSchema = object({
	value: string(),
	count: number(),
});

export type StringFacetValue = Output<typeof stringFacetValueSchema>;

/**
 * Corresponds to IntFacetValue in v1/models/rd_levels.py
 */
export const intFacetValueSchema = object({
	value: number(),
	count: number(),
});

export type IntFacetValue = Output<typeof intFacetValueSchema>;

/**
 * Corresponds to RDQueryResult in v1/models/rd_levels.py
 */
export const rdQueryResultSchema = object({
	levels: array(rdLevelSchema),
	tags: array(stringFacetValueSchema),
	artists: array(stringFacetValueSchema),
	authors: array(stringFacetValueSchema),
	difficulties: array(intFacetValueSchema),
});

export type RDQueryResult = Output<typeof rdQueryResultSchema>;
