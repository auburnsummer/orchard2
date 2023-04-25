import { LoaderArgs, redirect } from "@remix-run/node";
import { useLoaderData, useRouteError } from "@remix-run/react";
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

        // get the goodies out of the response.
        const {access_token, refresh_token, expires_in} = await resp.json();

        const authHeader = new Headers();
        authHeader.set("Authorization", `Bearer ${access_token}`);

        // next, check if the user exists. There's an API endpoint /user/me
        // that will return the user if they exist, or 404 if they don't.
        // If they don't exist, we'll need to create them, using the /user/create endpoint.
        // both these endpoints use an Authorization header with a Bearer token, which is the access_token from above.
        // we don't need to do anything if the user already exists.
        const userResp = await fetch(`${process.env.API_URL}/user/me`, {
            headers: authHeader
        });
        if (userResp.status === 404) {
            // create the user.
            // if the operation fails, please throw an error.
            const createResp = await fetch(`${process.env.API_URL}/user/create`, {
                method: "POST",
                headers: authHeader
            });
            if (!createResp.ok) {
                throw new Error("Failed to create user");
            }
        }

        // finally, redirect to the home page with the cookies set.
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

// we shouldn't get here, because the loader redirects to the home page.
export default function DiscordCallback() {
    const data = useLoaderData();
    return (
        <h1>Hello! {JSON.stringify(data)}</h1>
    )
}


export function ErrorBoundary() {
    const isError = (err: unknown): err is Error => err instanceof Error;

    const error = useRouteError();
    return isError(error)
        ? (
            <div>
                <h1>Oh no!</h1>
                <p>{error.message}</p>
            </div>
        ) 
        : (
            <div>
                <h1>Oh no!</h1>
                <p>Something went wrong.</p>
            </div>    
        )
}
