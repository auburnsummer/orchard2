import { LinksFunction } from "@remix-run/node";
import { Link, useMatches } from "@remix-run/react"
import { isDiscordUserObj } from "~/types/user";

import styles from "./profile.css";

export const links : LinksFunction = () => [
    {rel: "stylesheet", href: styles}
];

function NotLoggedIn() {

}

export default function ProfileRoute() {
    // get the loader data from the _base route using useMatches
    const data = useMatches().find(match => match.id === "routes/_base")?.data;

    console.log(data);

    if (isDiscordUserObj(data)) {
        console.log("made it here");
        const user = data.user;
        console.log(user);
        if (user) {
            return (
                <div className="pr">
                    <div className="pr_sidebar">
                        <div className="pr_name">
                            <span className="pr_username">{user.username}</span>
                            <span className="pr_discriminator">#{user.discriminator}</span>
                        </div>
                        <img className="pr_profile-pic" src={`https://cdn.discordapp.com/avatars/${user.id}/${user.avatar}.png`} />
                        <div className="pr_logout-container">
                            <Link className="pr_logout" to="/logout">Logout</Link>
                        </div>
                    </div>
                    <div className="pr_content">
                        <p>auburn here! there aren't any settings yet, so the only thing you can do here is log out.</p>
                        <p>i'll have some settings here in the future!</p>
                    </div>
                </div>
            )
        } else {
            return (
                <div>
                    <h1>You are not logged in, click the top right button to log in</h1>
                </div>
            )
        }
    }
  }