import { effect, signal } from '@preact/signals';
import { authToken$, notLoggedIn } from './auth';
import { type User, getLoggedInUser } from '~/api/auth';
import { type AsyncResource } from '~/hooks/useAsync';
import { getErrorMessage } from '~/utils/error';

export const loggedInUser$ = signal<AsyncResource<User> | typeof notLoggedIn>(notLoggedIn);

effect(async () => {
	// Any signal where the .value is read are marked as dependencies.
	// For our coding style, we're explicitly reading all intended deps at
	// the start of the effect with the void operator.
	// This is because deps that are read after an "await" won't be marked as
	// dependencies by Preact automatically. So it's safer to always "read"
	// all dependencies at the start.
	void authToken$.value;
	if (authToken$.value === notLoggedIn) {
		loggedInUser$.value = notLoggedIn;
	} else {
		// Fetch the user
		loggedInUser$.value = { state: 'loading' };
		try {
			const user = await getLoggedInUser(authToken$.value);
			loggedInUser$.value = { state: 'has data', data: user };
		} catch (error) {
			const message = await getErrorMessage(error);
			loggedInUser$.value = { state: 'has error', error, message };
		}
	}
});

export function logout() {
	loggedInUser$.value = notLoggedIn;
}
