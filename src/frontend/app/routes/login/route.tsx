import { redirect, LoaderArgs, ActionArgs } from "@remix-run/node";
import { isString } from "generic-type-guard";
import { createBackToCookie } from "~/utils/cookies";
import { getEnv } from "~/utils/env";

export const action = async ({request}: ActionArgs) => {
    const data = await request.formData();
    const method = data.get("method");
    const backTo = data.get("go_back_to");
    if (!method) {
        throw new Error("Code not found")
    }
    const headers = new Headers();

    if (backTo && isString(backTo)) {
        headers.append("set-cookie", await createBackToCookie(300).serialize(backTo))
    }

    if (method === "discord") {
        const searchParams = new URLSearchParams({
            client_id: getEnv("DISCORD_LOGIN_APPLICATION_ID") || '',
            redirect_uri: `${getEnv("SITE_URL")}/discord_callback`,
            response_type: 'code',
            scope: 'identify'
        })
        const discordLoginUrl = `https://discord.com/api/oauth2/authorize?${searchParams.toString()}`;
        return redirect(discordLoginUrl, {
            headers
        });
    }

    throw new Error("login method not supported");

}

export default function Login() {
    return redirect("/");
}