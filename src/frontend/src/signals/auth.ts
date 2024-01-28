import { effect, signal } from '@preact/signals';

export const notLoggedIn = Symbol('Value of authToken when user is not logged in');
type NotLoggedIn = typeof notLoggedIn;
const authTokenLocalStorageKey = 'orchard_auth_token';

const initialTokenValue = localStorage.getItem(authTokenLocalStorageKey) ?? notLoggedIn;

// Signals are kinda magical. So in this case I'm borrowing the rxjs convention of
// suffixing signals with a $. It's just a name, the $ doesn't change anything to the computer.
export const authToken$ = signal<string | NotLoggedIn>(initialTokenValue);

// Subscribe to changes made in other windows (i.e. the login popup)
addEventListener('storage', (event: StorageEvent) => {
	if (event.storageArea === localStorage) {
		console.log(event);
		// If storage.clear() is invoked, key and newValue are null
		if (event.key === null && event.newValue === null) {
			authToken$.value = notLoggedIn;
		}

		if (event.key === authTokenLocalStorageKey) {
			const newValue = event.newValue ?? notLoggedIn;
			authToken$.value = newValue;
		}
	}
});

// Write to LocalStorage when the value changes.
effect(() => {
	if (authToken$.value !== notLoggedIn) {
		localStorage.setItem(authTokenLocalStorageKey, authToken$.value);
	}
});
