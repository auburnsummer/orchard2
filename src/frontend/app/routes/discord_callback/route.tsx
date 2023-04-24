import { LoaderArgs, redirect } from "@remix-run/node";
import { useLoaderData } from "@remix-run/react";
import { createAuthCookie, createRefreshCookie } from "~/utils/cookies";


export const loader = async ({request}: LoaderArgs) => {
    // get a token and refresh token from the API.
    const url = new URL(request.url);
    const code = url.searchParams.get("code");
    const redirect_uri = `https://${url.hostname}/discord_callback`;
    if (code) {
        const resp = await fetch(`${process.env.API_URL}/auth/token`, {
            method: "POST",
            body: JSON.stringify({code, redirect_uri}),
            headers: {
                "content-type": "application/json"
            }
        });
        // once we have it, put it in the cookies!
        const {access_token, refresh_token, expires_in} = await resp.json();
        const authCookie = createAuthCookie(expires_in);
        const refreshCookie = createRefreshCookie();
        const headers = new Headers();
        headers.append("set-cookie", await authCookie.serialize(access_token))
        headers.append("set-cookie", await refreshCookie.serialize(refresh_token))
        return redirect("/", {
            headers
        });
    } else {
        throw new Error("Code not found in this callback");
    }
}

export default function DiscordCallback() {
    const data = useLoaderData();
    return (
        <h1>Hello! {JSON.stringify(data)}</h1>
    )
}

export function ErrorBoundary() {
    return (
        <h1>error</h1>
    )
}