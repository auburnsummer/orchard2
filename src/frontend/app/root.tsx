import { Links, Outlet } from "@remix-run/react";

import { Header, headerLinks } from "~/components/Header";

import baseStyles from "./root.css";

export const links = () => [
  ...headerLinks(),
  {rel: "stylesheet", href: baseStyles}
]

export default function Root() {
  return (
    <html lang="en">
      <head>
        <meta charSet="utf-8" />
        <title>Rhythm Café</title>
        <Links />
      </head>
      <body>
        <Header />
        <Outlet />
      </body>
    </html>
  );
}