import React from "react";

import { LinksFunction, LoaderArgs } from "@remix-run/node";
import { Outlet, useLoaderData } from "@remix-run/react";

import styles from "./_base.css";
import { Header } from "~/components/Header";
import { createAuthCookie } from "~/utils/cookies";
import { isUser } from "~/types/user";
import { getEnv } from "~/utils/env";

export const links : LinksFunction = () => [
  {rel: "stylesheet", href: styles}
]

export const loader = async ({request}: LoaderArgs) => {
    const authCookie = createAuthCookie();
    const value = await authCookie.parse(request.headers.get("cookie"));
    if (value) {
        try {
            const headers = new Headers();
            headers.set("Authorization", `Bearer ${value}`);
            const resp = await fetch(`${getEnv("API_URL")}/user/me`, {
                headers
            });
            const json = await resp.json();
            return { 
                user: isUser(json) ? json : null
            }
        }
        catch {
          // empty, if the token is invalid, we'll just return { user: null }
        }
    }
    return {
        user: null
    }
}

export default function BaseRoute() {
    const {user} = useLoaderData<typeof loader>();


    return (
        <div className="ba">
            <Header user={user} />
            <Outlet />
        </div>
    )
}