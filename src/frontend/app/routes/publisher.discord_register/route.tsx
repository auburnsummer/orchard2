import styles from "./publisher.discord_register.css"

import { ActionArgs, fetch, json, LinksFunction, redirect } from "@remix-run/node";
import { Link, useActionData, useSearchParams } from "@remix-run/react";
import { Button, Input } from "~/components/ui";
import { useState } from "react";
import { getEnv } from "~/utils/env";

export const links : LinksFunction = () => [
    {rel: "stylesheet", href: styles}
];

export async function action({ request }: ActionArgs) {
    const body = await request.formData();
    const guildToken = new URL(request.url).searchParams.get("guild_token");
    if (!guildToken) {
        const error = {
            error: true,
            message: "No guild token, try restarting the command"
        }
        return json(error, {status: 422})
    }
    const pubName = body.get("pub_name");
    if (!pubName) {
        const error = {
            error: true,
            message: "Publisher name cannot be blank."
        }
        return json(error, {status: 422})
    }
    const resp = await fetch(`${getEnv("API_URL")}/publisher/new/discord`, {
        method: "POST",
        headers: {
            "Authorization": `Bearer ${guildToken}`,
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "publisher_name": pubName
        })
    });
    if (resp.ok) {
        const contents = await resp.json();
        return json({"success": true, "id": contents["id"]})
    } else {
        const body = await resp.json();
        const message = body.message;
        const error = {
            error: true,
            message
        }
        return json(error, {status: 422})
    }
}

export default function PublisherRegisterNew() {
    const [buttonEnabled, setButtonEnabled] = useState(false);

    const onInputChange: React.ChangeEventHandler<HTMLInputElement> = (evt) => {
        const value = evt.target.value;
        if (value.length > 0) {
            setButtonEnabled(true);
        } else {
            setButtonEnabled(false);
        }
    };

    const data = useActionData<typeof action>();

    const internalContent = data && "success" in data ? (
        <p className="rn_successful">
            Creation of publisher successful. id: {data.id}
        </p>
    ) : (
        <>
            {
                data?.error && (
                    <p className="rn_error">
                        {data.message}
                    </p>
                )
            }
            <form className="rn_form" method="post">
                <label className="rn_l1" htmlFor="pub_name">
                    Publisher name*:
                </label>
                <Input type="text" name="pub_name" className="rn_nameinput" onChange={onInputChange} />
                <Button type="submit" value="Submit" className="rn_button" disabled={!buttonEnabled}>Submit</Button>
            </form>
            <p className="rn_hint">
                *This is typically the name of the discord server. You can change this at any time.
            </p>
        </>
    )

    return (
        <div className="rn">
            <div className="rn_content">
                {internalContent}
            </div>
        </div>
    )
}