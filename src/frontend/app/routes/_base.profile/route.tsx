import { LinksFunction } from "@remix-run/node";
import { Link, useMatches } from "@remix-run/react"
import { isUser, isUserObject } from "~/types/user";

import styles from "./profile.css";

export const links : LinksFunction = () => [
    {rel: "stylesheet", href: styles}
];

export default function ProfileRoute() {
    // get the loader data from the _base route using useMatches
    const data = useMatches().find(match => match.id === "routes/_base")?.data;

    if (isUserObject(data)) {
        const user = data.user;
        if (user) {
            return (
                <div className="pr">
                    <div className="pr_sidebar">
                        <div className="pr_name">
                            <span className="pr_username">{user.name}</span>
                        </div>
                        <img className="pr_profile-pic" src={user.avatar_url} />
                        <div className="pr_logout-container">
                            <Link className="pr_logout" to="/logout">Logout</Link>
                        </div>
                    </div>
                    <div className="pr_content">
                        <div className="pr_settings">
                            <p>(auburn here. there aren't any settings yet, so the only thing you can do here is log out.)</p>
                            <p>(i'll have some settings here in the future!)</p>
                        </div>
                        <div className="pr_userid">
                            <p>user id: {user.id}</p>
                        </div>
                    </div>

                </div>
            )
        } else {
            return (
                <div className="pr">
                    <h1>You are not logged in, click the top right button to log in</h1>
                </div>
            )
        }
    }
}