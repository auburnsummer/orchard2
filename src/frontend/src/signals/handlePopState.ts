// https://developer.mozilla.org/en-US/docs/Web/API/Window/popstate_event
// When the user hits back, a popstate is emitted. we should handle this by triggering a search.
// nb: if the user changes the URL query params manually, an actual URL navigation happens in the browser; we don't need to do anything special.

import { getRDSearchParams, rdSearchParams$ } from './searchParams';
import { fetchResults$ } from './searchResults';

export const registerPopStateHandler = () => {
	window.addEventListener('popstate', () => {
		rdSearchParams$.value = getRDSearchParams();
		void fetchResults$.value(false);
	});
};
