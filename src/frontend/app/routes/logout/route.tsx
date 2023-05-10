import { redirect, LoaderArgs } from "@remix-run/node";
import { createAuthCookie } from "~/utils/cookies";

export const loader = async ({request}: LoaderArgs) => {
    // read the token from the cookie.
    // if it's not there, redirect to the home page.
    // if it is there, call the /auth/revoke endpoint.
    // after calling the endpoint, clear the cookies, without waiting for the response.
    // then redirect to the login page.
    const authCookie = createAuthCookie();
    const value = await authCookie.parse(request.headers.get("cookie"));
    if (value) {
        try {
            const headers = new Headers();
            headers.set("Authorization", `Bearer ${value}`);
            await fetch(`${process.env.API_URL}/auth/revoke`, {
                method: "POST",
                headers
            });
        }
        catch {
            // empty, if the token is invalid, we'll just return { user: null }
        }
        const headers = new Headers();
        headers.append("set-cookie", await authCookie.serialize("deleted", {maxAge: -1}));

        return redirect("/", { headers });
    }
}