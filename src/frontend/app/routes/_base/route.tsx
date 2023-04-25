import { LinksFunction, LoaderArgs } from "@remix-run/node";
import { Outlet, useLoaderData } from "@remix-run/react";
import { Header, headerLinks, isDiscordUser } from "~/components/Header";
import { createAuthCookie } from "~/utils/cookies";

import styles from "./_base.css";

export const links : LinksFunction = () => [
  ...headerLinks(),
  {rel: "stylesheet", href: styles}
]

export const loader = async ({request}: LoaderArgs) => {
  const authCookie = createAuthCookie();
  const value = await authCookie.parse(request.headers.get("cookie"));
  if (value) {
    try {
      const headers = new Headers();
      headers.set("Authorization", `Bearer ${value}`);
      const resp = await fetch(`${process.env.API_URL}/user/me`, {
        headers
      });
      const json = await resp.json();
      return {
        user: isDiscordUser(json) ? json : null
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