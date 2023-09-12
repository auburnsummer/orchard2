import { LoaderArgs, redirect } from "@remix-run/node";
import { createAuthCookie, createBackToCookie } from "~/utils/cookies";
import { getEnv } from "~/utils/env";


export const loader = async ({request}: LoaderArgs) => {
    const url = new URL(request.url);
    const code = url.searchParams.get("code");
    if (!code) {
        throw new Error("Code not found")
    }
    const API_URL = getEnv("API_URL");
    const BASE_URL = getEnv("SITE_URL");
    const redirect_uri = `${BASE_URL}/discord_callback`;
    console.log(redirect_uri);

    const resp = await fetch(`${API_URL}/auth/token/discord`, {
        method: "POST",
        body: JSON.stringify({code, redirect_uri}),
        headers: {
            "content-type": "application/json"
        }
    });
    if (!resp.ok) {
        const text = await resp.text();
        throw new Error(text);
    }
    // get the goodies out of the response.
    const {token, expires_in} = await resp.json();


    // redirect to the page set by the cookie earlier.
    // if there isn't one, just redirect to home page.
    const pageToDirectTo = (await createBackToCookie().parse(request.headers.get("cookie"))) ?? "/"
    
    // set a cookie.
    const authCookie = createAuthCookie(expires_in);
    const headers = new Headers();
    headers.append("set-cookie", await authCookie.serialize(token))
    return redirect(pageToDirectTo, {
        headers
    });
}