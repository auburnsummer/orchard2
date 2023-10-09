import styles from "./_base.publisher_.add.css";

import { LinksFunction, ActionArgs, json } from "@remix-run/node";
import { createAuthCookie } from "~/utils/cookies";
import { getEnv } from "~/utils/env";
import { isPrefillResult } from "~/utils/level";
import { useLoaderData, useRouteError } from "@remix-run/react";
import { bail, isOrchardError } from "~/utils/error";
import { wrappedFetch } from "~/utils/fetch";

export const links : LinksFunction = () => [
    {rel: "stylesheet", href: styles}
];

export async function loader({ request }: ActionArgs) {
    const authCookie = createAuthCookie();
    const value = await authCookie.parse(request.headers.get("cookie"));
    if (!value) {
        bail({
            error_code: "PleaseLogInFirst",
            message: "You need to be logged in first"
        })
    }
    const url = new URL(request.url);
    const publisherToken = url.searchParams.get("publisher_token");

    const resp = await wrappedFetch(`${getEnv("API_URL")}/level/prefill`, {
        method: "POST",
        headers: {
            "Authorization": `Bearer ${value},Bearer ${publisherToken}`
        }
    });
    if (resp.ok) {
        const contents = await resp.json();
        if (isPrefillResult(contents)) {
            return json(contents);
        } else {
            bail({
                error_code: "PrefillResultDidNotMatchSchema",
                message: "If you're seeing this, it's a bug. please ping auburn!"
            });
        }
    } else {
        bail({
            error_code: "UnknownError",
            message: await resp.text()
        })
    }
}

export function ErrorBoundary() {
    const error = useRouteError();

    console.log(error);

    const typedError = isOrchardError(error.data) ? error : {
        error_code: "UnknownError",
        message: `${error}`
    }

    return (
        <p>{JSON.stringify(typedError)}</p>
    )
}

export default function PublisherAddPrefillMenu() {
    const result = useLoaderData<typeof loader>();


    return (
        <p>{JSON.stringify(result)}</p>
    )
}