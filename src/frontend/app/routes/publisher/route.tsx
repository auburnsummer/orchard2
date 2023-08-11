import { LinksFunction } from "@remix-run/node";
import { Outlet } from "@remix-run/react";
import React from "react";
import { PublisherHeader } from "~/components/PublisherHeader";

import styles from "./publisher.css";

export const links : LinksFunction = () => [
    {rel: "stylesheet", href: styles}
];

export default function Publisher() {
    return (
        <div className="pu">
            <PublisherHeader />
            <Outlet />
        </div>
    )
}