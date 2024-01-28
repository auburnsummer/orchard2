import { Button } from '~/ui';
import { getEnv } from '~/utils/env.js';

const redirectUri = window.location.origin + '/discord_callback';

const searchParameters = new URLSearchParams({
	/* eslint-disable @typescript-eslint/naming-convention */
	client_id: getEnv('VITE_DISCORD_APPLICATION_ID'),
	redirect_uri: redirectUri,
	response_type: 'code',
	scope: 'identify',
	/* eslint-enable @typescript-eslint/naming-convention */
});

const discordLoginUrl = `https://discord.com/api/oauth2/authorize?${searchParameters.toString()}`;

export function LoginButton() {
	const onClick = () => {
		window.open(discordLoginUrl, '_blank', 'popup=true,width=800,height=800');
	};

	return (
		<Button onClick={onClick} class='lu'>
            Log in
		</Button>
	);
}
