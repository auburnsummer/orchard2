import { Button } from "@orchard/ui";

const redirectUri = window.location.origin + "/discord_callback";

const searchParams = new URLSearchParams({
    client_id: import.meta.env.VITE_DISCORD_APPLICATION_ID,
    redirect_uri: redirectUri,
    response_type: 'code',
    scope: 'identify'
});

const discordLoginUrl = `https://discord.com/api/oauth2/authorize?${searchParams.toString()}`;

export function LoginButton() {
    return (
        <Button href={discordLoginUrl} target="_blank">
            Log in
        </Button>
    )
}