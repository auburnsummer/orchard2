import { computed, signal } from '@preact/signals';
import { objectEntries } from 'ts-extras';
import { safeParse } from 'valibot';
import { DEFAULT_SEARCH_PARAMS, keyOfDefaultSearchParamsSchema, rdSearchParams$ } from './searchParams';
import { type RDQueryResult } from '~/api/levels/schemas';
import { type AsyncResource } from '~/hooks/useAsync';
import { searchRDLevels } from '~/api/levels/levels';
import { getErrorMessage } from '~/utils/error';
import { serializeObjectToSearchParams } from '~/utils/url';

export const rdSearchResults$ = signal<AsyncResource<RDQueryResult>>({ state: 'loading' });
export const previousSearchResults$ = signal<RDQueryResult | undefined>(undefined);

export const fetchResults$ = computed(() => {
	const rdSearchParams = rdSearchParams$.value;
	const currentRdSearchResults = rdSearchResults$.value;
	return async (writeToQueryParams: boolean) => {
		if (writeToQueryParams) {
			const newSearchParams = serializeObjectToSearchParams(rdSearchParams);
			const url = new URL(window.location.href);
			// Replace the search params with our ones. but keep anything in the original we didn't know about.
			for (const key of newSearchParams.keys()) {
				url.searchParams.delete(key);
			}

			for (const [key, value] of newSearchParams.entries()) {
				url.searchParams.append(key, value);
			}

			window.history.pushState({}, '', url);
		}

		if (currentRdSearchResults.state === 'has data') {
			previousSearchResults$.value = currentRdSearchResults.data;
		}

		rdSearchResults$.value = { state: 'loading' };
		try {
			const queryResult = await searchRDLevels(rdSearchParams);
			rdSearchResults$.value = {
				state: 'has data',
				data: queryResult,
			};
		} catch (error) {
			const errorMessage = await getErrorMessage(error);
			rdSearchResults$.value = {
				state: 'has error',
				error,
				message: errorMessage,
			};
		}
	};
});

export const searchResultsLoading$ = computed(() => rdSearchResults$.value.state === 'loading');

/**
 * Equal to rdSearchResults when it has a value. when rdSearchResults is loading, this is
 * equal to previousSearchResults. If neither of these are available, it's a loading state.
 */
export const searchResultsCombined$ = computed<AsyncResource<RDQueryResult>>(() => {
	const rdSearchResults = rdSearchResults$.value;
	const previousSearchResults = previousSearchResults$.value;
	if (rdSearchResults.state === 'has data' || rdSearchResults.state === 'has error') {
		return rdSearchResults;
	}

	if (previousSearchResults) {
		return {
			state: 'has data',
			data: previousSearchResults,
		};
	}

	return {
		state: 'loading',
	};
});

void fetchResults$.value(false);
