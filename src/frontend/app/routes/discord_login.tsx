import { redirect } from "@remix-run/node";

export const loader = async () => {
    const resp = await fetch(`${process.env.API_URL}/auth/client_id`);
    if (resp.ok) {
        const client_id: string = await resp.json();
        const redirect_uri = encodeURIComponent("https://3000.cs.lulu.auburn.dev")
        return redirect(`https://discord.com/api/oauth2/authorize?client_id=${client_id}&redirect_uri=${redirect_uri}&response_type=code&scope=identify%20guilds.members.read`)
    } else {
        let err = new Error("HTTP status code: " + resp.status)
        err.cause = resp;
        throw err
    }
}