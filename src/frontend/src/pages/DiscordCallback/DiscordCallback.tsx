import { useEffect } from 'preact/hooks';
import './DiscordCallback.css';
import { authToken$ } from '~/signals/auth';
import { useAsyncAction } from '~/hooks/useAsync';
import { getOrchardTokenResponseFromDiscord } from '~/api/auth';
import { Icon } from '~/ui';
import { Loading } from '~/components/Loading';

function DiscordCallbackContents() {
	const [output, startLoginAttempt] = useAsyncAction(async (code: string | undefined) => {
		if (!code) {
			throw new Error('Expected a code query parameter.');
		}

		return getOrchardTokenResponseFromDiscord(code);
	});
	useEffect(() => {
		if (output.state === 'not started') {
			const urlParameters = new URLSearchParams(window.location.search);
			const code = urlParameters.get('code') ?? undefined;
			startLoginAttempt(code);
		}

		if (output.state === 'has data') {
			authToken$.value = output.data.token;
			setTimeout(window.close, 1000);
		}
	}, [output]);

	if (output.state === 'not started' || output.state === 'loading') {
		return (
			<Loading class='dc_loading' text='Logging in...'/>
		);
	}

	if (output.state === 'has error') {
		return (
			<div class='dc_error'>
				<Icon class='dc_error-icon' name='exclamation-triangle' />
				<span class='dc_error-text'><b>Error:</b> {output.message}</span>
				<span class='dc_error-advice'>Please try closing this window and logging in again. If this error persists, ping Auburn, thanks!</span>
			</div>
		);
	}

	// Must have data if we got here.
	return (
		<div class='dc_success'>
			<Icon class='dc_success-icon' name='check-circle' />
			<span class='dc_success-text'>Log in successful! This page will close automatically.</span>
		</div>
	);
}

export function DiscordCallback() {
	return (
		<div class='dc'>
			<DiscordCallbackContents />
		</div>
	);
}
