import { redirect, LoaderArgs } from "@remix-run/node";

export const loader = async ({request}: LoaderArgs) => {
    const url = new URL(request.url);

    // Endpoint that exposes the client_id of the app.
    // This is so that only the backend needs to have Discord environment vars configured, and the frontend
    // fetches from the backend to get that.
    const resp = await fetch(`${process.env.API_URL}/auth/client_id`);
    if (resp.ok) {
        const client_id: string = await resp.json();
        const redirect_uri = encodeURIComponent(`https://${url.hostname}/discord_callback`)
        return redirect(`https://discord.com/api/oauth2/authorize?client_id=${client_id}&redirect_uri=${redirect_uri}&response_type=code&scope=identify%20guilds.members.read`)
    } else {
        let err = new Error("HTTP status code: " + resp.status)
        err.cause = resp;
        throw err
    }
}