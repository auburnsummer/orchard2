import { redirect, LoaderArgs } from "@remix-run/node";
import { createAuthCookie } from "~/utils/cookies";
import { getEnv } from "~/utils/env";

export const loader = async ({request}: LoaderArgs) => {
    const url = new URL(request.url);
    const method = url.searchParams.get("method");
    if (!method) {
        throw new Error("Code not found")
    }
    if (method === "discord") {
        const searchParams = new URLSearchParams({
            client_id: getEnv("DISCORD_LOGIN_APPLICATION_ID") || '',
            redirect_uri: `${getEnv("SITE_URL")}/discord_callback`,
            response_type: 'code',
            scope: 'identify'
        })
        const discordLoginUrl = `https://discord.com/api/oauth2/authorize?${searchParams.toString()}`;
        return redirect(discordLoginUrl);
    }

    throw new Error("login method not supported");
}

export default function Login() {
    return redirect("/");
}