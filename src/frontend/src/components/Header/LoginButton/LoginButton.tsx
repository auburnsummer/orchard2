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
    const onClick = () => {
        window.open(discordLoginUrl, "_blank", "popup=true,width=800,height=800")
    }

    return (
        <Button onClick={onClick} class="lb">
            Log in
        </Button>
    )
}