import React from "react";
import cc from "clsx";

import { WithClass } from "~/utils/types";

import sample from "just-random";

type HeaderProps = WithClass & {
    user: User | null;
}

import "./Header.css";
import { User } from "~/utils/user";
import { Form, Link, useLocation } from "@remix-run/react";

const EBOOKS = [
    'Klyzx: CV why are you streaming a green line for the entire day',
    '9thCore: most levels arent gonna have the entirety of bad apple recreated with 4x4 pixel bean decos',
    'fizzd: banana detection',
    'Nocallia: the macarena is syncopation',
    'giacomo: ok, that\'s good news\ngiacomo: i have no idea whats going on',
    'fizzd: gamedev is like: we announce game, sleep for 1 year and then wake up and press the release button',
    'fizzd: by fixed i mean "off" has been changed to "oof"',
    'Maddy: i only know how to make a box that says fuck in javascript but ok',
    'DNH: just use -- snap\nDNH: dont be a coward',
    'okamii: i needed four different pitches of beep so i made 24 instead',
    'roninnozlo: horny anthem\nSome J Name: what>\nSome J Name: no\nSome J Name: i have never charted a horny song in my life',
    'MarioMak967: you all are about as competent as the RHS',
    'Kin: ah, the 🅱️iolin',
    'Fritzy: wait there are other video games',
    'notDonte: screw kpop in this discord we stan xeno',
    'CV35W: Then the teacher was talking about Maple Leaf Rag and said "so this is that era\'s equivalent of a slap" and I woke up again',
    'plastermaster: chat is going so fast nobody will realize I love you guys',
    'lugi: lucia has been trapped in the RDCube™️\nlugi: she must atone',
    'Szprycha: dang that fall looked real nasty\nsquareshots? insomniac cues? freezeshots? the hell are you talking about? come on let\'s go play Unwell and see who survives the longest',
    'noche: if i could pin "MORE DEATH, MORE BLOOD, MORE COWBELL" without using up 3 pin slots i would',
    'megaminerzero: The animator falls over like 𝚎𝚊𝚜𝚎: 𝚕𝚒𝚗𝚎𝚊𝚛'
];


type ProfileProps = {
    user: User | null;
}
const Profile = ({user}: ProfileProps) => {
    const location = useLocation();

    if (!user) {
        return (
            <Form action="/login" method="post">
                <input type="hidden" id="input_method" name="method" value="discord" />
                <input type="hidden" id="input_go_back_to" name="go_back_to" value={`${location.pathname}${location.search}`} />
                <button type="submit" className="he_not-logged-in">Log in</button>
            </Form>
        )
    } else {
        return (
            <Link to="/profile" className="he_logged-in" title={`${user.name}`}>
                <img className="he_profile-pic" src={user.avatar_url} />
            </Link>
        )
    }

}

export function Header({className, user} : HeaderProps) {
    const ebook = sample(EBOOKS);
    return (
        <div className={cc(className, "he")}>
            <Link to="/" title={ebook}>
                <svg
                fillRule="evenodd"
                strokeLinejoin="round"
                strokeMiterlimit={2}
                className="he_logo"
                clipRule="evenodd"
                viewBox="0 0 391 59"
                >
                    <path
                        fillRule="nonzero"
                        d="M22.2 14.1v9.6h-4.9c-2.2 0-3.9.6-5 1.8-1 1.2-1.6 3-1.6 5.4v15.9H.7V14h7l1.6 4c1.1-1.3 2.5-2.3 4-3a14 14 0 0 1 5.3-.9h3.5zm25.4-1c4 0 7.3 1.2 9.5 3.6 2.3 2.4 3.3 6 3.3 10.5v19.6h-10V29c0-2.4-.5-4-1.4-5.3a5.3 5.3 0 0 0-4.2-1.7c-2 0-3.7.7-4.9 2.2a10.4 10.4 0 0 0-1.9 6.6v15.9H28v-47h10v16.7c2.7-2.2 5.9-3.4 9.6-3.4zm53.9 1L88.5 46c-2 4.8-4.4 8.2-7 10.2-2.6 2-6 3-10.4 3h-3.6v-9h3.3c2 0 3.5-.3 4.4-.8.8-.6 1.6-1.8 2.5-3.7L64.2 14.1h11l7.9 19.5 7.7-19.5h10.7zm27.2 23.7v9H122c-9 0-13.4-4.6-13.4-13.7V22.8h-6.4v-8.7h6.7l1.5-8h8.2v8h9.9v8.7h-10v10c0 1.7.5 3 1.4 3.8.8.8 2 1.2 3.7 1.2h5zm26.4-24.7c4 0 7.2 1.2 9.5 3.6 2.2 2.4 3.3 6 3.3 10.5v19.6h-10V29c0-2.4-.5-4-1.5-5.3a5.3 5.3 0 0 0-4.1-1.7c-2 0-3.7.7-5 2.2a10.4 10.4 0 0 0-1.8 6.6v15.9h-10v-47h10v16.7c2.6-2.2 5.8-3.4 9.6-3.4zm60.1 0c3.6 0 6.6 1.2 8.7 3.5 2.1 2.4 3.2 5.7 3.2 10v20.2h-10V28.3a8 8 0 0 0-1.2-4.7c-.8-1-2-1.5-3.5-1.5a5 5 0 0 0-4.1 2 8.6 8.6 0 0 0-1.7 5.5v17.2h-10V28.3c0-2-.3-3.7-1.2-4.7-.8-1-2-1.5-3.5-1.5a5 5 0 0 0-4.1 2 8.6 8.6 0 0 0-1.7 5.5v17.2h-10V14h7l1.6 3.5c1.2-1.4 2.7-2.5 4.4-3.3 1.8-.8 3.6-1.2 5.6-1.2 2.3 0 4.2.4 5.9 1.3 1.7.9 3 2.2 4 3.8 1.3-1.6 2.8-2.9 4.6-3.8 1.8-.9 3.9-1.3 6-1.3zm53.1 34.7c-3.6 0-6.6-.8-9.4-2.3a17 17 0 0 1-8.6-15c0-3.3.7-6.3 2.3-9 1.4-2.6 3.6-4.7 6.4-6.2 2.7-1.4 5.8-2.2 9.3-2.2 3 0 5.8.6 8.3 1.8a16.7 16.7 0 0 1 9.4 12h-10a8.4 8.4 0 0 0-3-3.6 8.6 8.6 0 0 0-4.6-1.2c-2.3 0-4.2.7-5.7 2.3a8.5 8.5 0 0 0-2.3 6.1c0 2.5.7 4.5 2.3 6a8 8 0 0 0 5.9 2.3 8 8 0 0 0 4.4-1.3c1.3-.8 2.3-2 3-3.6h10c-1 4.2-3 7.5-6.1 10-3.1 2.6-7 3.9-11.6 3.9zm39.4-34.7c4.8 0 8.4 1.2 11 3.6 2.5 2.4 3.8 5.7 3.8 10.2v19.9h-6.9l-1.5-3.4c-2.7 3-6.3 4.4-10.8 4.4-3.8 0-6.8-1-8.9-2.7a9 9 0 0 1-3.2-7.3c0-3.3 1.2-5.8 3.4-7.6 2.2-1.8 5.5-2.7 9.7-2.7h8.2v-1.3c0-1.6-.4-3-1.2-3.8-.9-.8-2.2-1.2-3.8-1.2-1.4 0-2.6.3-3.5 1-1 .7-1.5 1.6-1.7 2.7h-10c.5-3.7 2.2-6.6 4.9-8.7 2.7-2 6.2-3.1 10.5-3.1zm-2 26.6a8 8 0 0 0 5.1-1.4c1.2-1 1.7-2.2 1.7-3.8V34h-7c-2.7 0-4 1-4 2.8 0 .9.3 1.6 1 2 .7.7 1.7 1 3.2 1zM352 22.8h-8.5v24h-10v-24H327v-8.7h6.4v-3c0-7.5 3.6-11.2 11-11.2h7.5v8.7h-5.2c-1.2 0-2 .2-2.5.7-.6.6-.8 1.4-.8 2.5v2.3h8.6v8.7zm38.8 7.3c0 1.5 0 2.6-.2 3.3H365a7.7 7.7 0 0 0 2.7 4.7c1.4 1.1 3.2 1.6 5.3 1.6 3.1 0 5.4-1 6.8-3H390c-1.2 3.3-3.3 6-6.3 8s-6.6 3-10.8 3c-3.6 0-6.6-.7-9.4-2.2a15.6 15.6 0 0 1-6.3-6.2 17.2 17.2 0 0 1-2.3-8.9c0-3.2.7-6.2 2.3-8.9 1.4-2.6 3.6-4.7 6.3-6.2 2.7-1.4 5.8-2.2 9.2-2.2 3.5 0 6.6.7 9.4 2.2a16.4 16.4 0 0 1 8.6 14.8zm-17.8-9c-1.9 0-3.4.6-4.8 1.5a8.4 8.4 0 0 0-2.9 4.3h15.3c-1.1-3.8-3.6-5.7-7.6-5.7z"
                    />
                </svg>
            </Link>
            <div aria-hidden className="he_spacer" />
            <div className="he_profile">
                <Profile user={user} />
            </div>

        </div>

    )
}