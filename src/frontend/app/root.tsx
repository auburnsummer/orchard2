import { cssBundleHref } from "@remix-run/css-bundle";
import { json, LinksFunction } from "@remix-run/node";
import {
    isRouteErrorResponse,
  Links,
  LiveReload,
  Meta,
  Outlet,
  Scripts,
  ScrollRestoration,
  useLoaderData,
  useRouteError,
} from "@remix-run/react";

import "the-new-css-reset/css/reset.css";
// nunito for titles, big text
import "@fontsource-variable/nunito/index.css";
// nunito sans for smaller text
import "@fontsource-variable/nunito-sans/index.css";
// Zen Maru Gothic for Chinese / Japanese
import "@fontsource/zen-maru-gothic/400.css"
// TODO: check Korean
import "./shared.css";
import type { Environment } from "./globals";
import { NotFound } from "./components/NotFound/NotFound";
import { isOrchardError } from "./utils/error";

export const links: LinksFunction = () => [
  ...(cssBundleHref ? [{ rel: "stylesheet", href: cssBundleHref }] : []),
];

export async function loader() {
    const ENV: Environment = {
        SITE_URL: process.env.SITE_URL || '',
        DISCORD_LOGIN_APPLICATION_ID: process.env.DISCORD_LOGIN_APPLICATION_ID || '',
        API_URL: process.env.API_URL || ''
    };
    return json({
        ENV
    });
}

export const shouldRevalidate = () => false;

export default function App() {
    const data = useLoaderData<typeof loader>();

    return (
        <html lang="en">
            <head>
                <meta charSet="utf-8" />
                <meta name="viewport" content="width=device-width,initial-scale=1" />
                <Meta />
                <Links />
            </head>
            <body>
                <Outlet />
                <script
                    dangerouslySetInnerHTML={{
                        __html: `window.ENV = ${JSON.stringify(
                            data.ENV
                        )}`,
                    }}
                />
                <ScrollRestoration />
                <Scripts />
                <LiveReload />
            </body>
        </html>
    );
}

export function ErrorBoundary() {
    const error = useRouteError();

    // handle 404 specifically.
    if (isRouteErrorResponse(error)) {
        const statusCode = error.status;
        if (statusCode == 404) {
            return (
                <html lang="en">
                <head>
                    <Meta />
                    <Links />
                </head>
                    <body>
                        <NotFound />
                        <ScrollRestoration />
                        <Scripts />
                        <LiveReload />
                    </body>
                </html>
            )
        }
    }

    // Don't forget to typecheck with your own logic.
    // Any value can be thrown, not just errors!
    let errorMessage = "Unknown error";
    if (error instanceof Error) {
        errorMessage = error.message;
    }
    if (isRouteErrorResponse(error)) {
        errorMessage = error.data;
    }
    if (isOrchardError(error)) {
        errorMessage = `${error.error_code}: error.message`;
    }

    return (
        <html lang="en">
            <head>
                <Meta />
                <Links />
            </head>
            <body>
                <div className="err">
                    <h1>Uh oh ...</h1>
                    <p>Something went wrong.</p>
                    <p>This is the root error handler. If you're seeing this...</p>
                    <p>...it means an error occured that I did not anticipate.</p>
                    <p>If you keep seeing this, please ping auburn! thanks 🙏</p> 
                    <pre>{errorMessage}</pre>
                </div>
                <ScrollRestoration />
                <Scripts />
                <LiveReload />
            </body>
        </html>
    );
}