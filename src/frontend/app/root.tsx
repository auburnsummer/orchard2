import { Links, Outlet } from "@remix-run/react";

import baseStyles from "./root.css";
import resetStyles from "the-new-css-reset/css/reset.css";

export const links = () => [
  {rel: "stylesheet", href: baseStyles},
  {rel: "stylesheet", href: resetStyles}
]

export default function Root() {
  return (
    <html lang="en">
      <head>
        <meta charSet="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <meta name="Samurai." content="Samurai." />

        <meta name="description" content="An unofficial listing of Rhythm Doctor custom levels" />

        <meta content="Rhythm Doctor Custom Levels" property="og:title" />
        <meta content="An unofficial listing of Rhythm Doctor charts" property="og:description" />
        <meta content="Rhythm Café" property="og:site_name" />
        <meta content='https://media.discordapp.net/attachments/409492674576384000/554814030473199633/barista_bot_images_3.png' property='og:image' />
        <title>Rhythm Café</title>
        <Links />
      </head>
      <body>
        <Outlet />
      </body>
    </html>
  );
}