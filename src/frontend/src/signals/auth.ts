import { effect, signal } from '@preact/signals';

const notLoggedIn = Symbol('Value of authToken when user is not logged in');
type NotLoggedIn = typeof notLoggedIn;
const authTokenLocalStorageKey = 'orchard_auth_token';

const initialTokenValue = localStorage.getItem(authTokenLocalStorageKey) ?? notLoggedIn;
export const authTokenSig = signal<string | NotLoggedIn>(initialTokenValue);

// Subscribe to changes made in other windows (i.e. the login popup)
addEventListener('storage', (event: StorageEvent) => {
	if (event.storageArea === localStorage) {
		// If storage.clear() is invoked, key and newValue are null
		if (event.key === null && event.newValue === null) {
			authTokenSig.value = notLoggedIn;
		}

		if (event.key === authTokenLocalStorageKey) {
			const newValue = event.newValue ?? notLoggedIn;
			authTokenSig.value = newValue;
		}
	}
});

// Write to LocalStorage when the value changes.
effect(() => {
	if (authTokenSig.value !== notLoggedIn) {
		localStorage.setItem(authTokenLocalStorageKey, authTokenSig.value);
	}
});
