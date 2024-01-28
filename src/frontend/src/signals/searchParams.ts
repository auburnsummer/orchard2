import { signal } from '@preact/signals';
import { type Draft, produce } from 'immer';
import { objectKeys } from 'ts-extras';
import { keyof, literal, picklist } from 'valibot';
import { type RDSearchParams } from '~/api/levels/schemas';

export const DEFAULT_SEARCH_PARAMS = {
	min_approval: 10,
};

export const keyOfDefaultSearchParamsSchema = picklist(objectKeys(DEFAULT_SEARCH_PARAMS));

const getSearchParams = () => new URLSearchParams(window.location.search);

const functionGet = <T>(key: string, transformFunction: (v: string) => T, fallback?: T) => {
	const value = getSearchParams().get(key);
	if (!value) {
		return fallback;
	}

	return transformFunction(value);
};

const functionArrayGet = <T>(key: string, transformFunction: (v: string) => T) => {
	const values = getSearchParams().getAll(key);

	return values.map(s => transformFunction(s));
};

const stringGet = (key: string) => functionGet(key, v => v);
const stringArrayGet = (key: string) => functionArrayGet(key, v => v);
const floatGet = (key: string) => functionGet(key, Number.parseFloat);
const intGet = (key: string) => functionGet(key, v => Number.parseInt(v, 10));
const intArrayGet = (key: string) => functionArrayGet(key, v => Number.parseInt(v, 10));
const booleanGet = (key: string) => functionGet(key, v => v.toLowerCase() === 'true');

export const rdSearchParams$ = signal<RDSearchParams>({
	q: stringGet('q'),
	tags: stringArrayGet('tags'),
	artists: stringArrayGet('artists'),
	authors: stringArrayGet('authors'),
	min_bpm: floatGet('min_bpm'),
	max_bpm: floatGet('max_bpm'),
	difficulty: intArrayGet('difficulty'),
	single_player: booleanGet('single_player'),
	two_player: booleanGet('two_player'),
	has_classics: booleanGet('has_classics'),
	has_oneshots: booleanGet('has_oneshots'),
	has_squareshots: booleanGet('has_squareshots'),
	has_freezeshots: booleanGet('has_freezeshots'),
	has_freetimes: booleanGet('has_freetimes'),
	has_holds: booleanGet('has_holds'),
	has_skipshots: booleanGet('has_skipshots'),
	has_window_dance: booleanGet('has_window_dance'),
	uploader: stringGet('uploader'),
	publisher: stringGet('publisher'),
	min_approval: intGet('min_approval') ?? DEFAULT_SEARCH_PARAMS.min_approval,
	max_approval: intGet('max_approval'),
	offset: intGet('offset'),
	limit: intGet('limit'),
});

export const setSearchParams = (draftFunc: (draft: Draft<RDSearchParams>) => void) => {
	rdSearchParams$.value = produce(rdSearchParams$.value, draftFunc);
};
