import styles from "./publisher.discord_register.css";

import { LinksFunction } from "@remix-run/node";
import { Link, useSearchParams } from "@remix-run/react";

export const links : LinksFunction = () => [
    {rel: "stylesheet", href: styles}
];


export default function PublisherRegister() {
    const [searchParams,] = useSearchParams();

    const newLink = `/publisher/discord_register/new?${searchParams.toString()}`;
    const linkLink = `/publisher/discord_register/link?${searchParams.toString()}`;

    return (
        <div className="re">
            <div className="re_content">
                <h2 className="re_title">Please select an option:</h2>
                <ol className="re_list">
                    <li>
                        <Link to={newLink} className="re_option re_new">
                            Create a new publisher for this server
                        </Link>
                    </li>
                    <li>
                        <Link to={linkLink} className="re_option re_link">
                            Link an existing publisher to this server
                        </Link>
                    </li>
                </ol>
                <p className="re_hint">If you're not sure, choose the first option.</p>
            </div>
        </div>
    )
}