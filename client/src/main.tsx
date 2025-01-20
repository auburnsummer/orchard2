import React from "react";
import ReactDOM from "react-dom/client";
import * as DjangoBridge from "@django-bridge/react";
import { CSRFTokenContext } from "@cafe/hooks/useCSRFToken";
import HomeView from "./views/HomeView";
import '@mantine/core/styles.css';
import '@mantine/notifications/styles.css';
import './style.css';

import { UserContext } from "@cafe/hooks/useUser";
import { ProfileView } from "./views/ProfileView/ProfileView";
import { Prelude } from "./components/Prelude/Prelude";
import { CreateClubView } from "./views/CreateClubView/CreateClub";


const config = new DjangoBridge.Config();

const views: { [key: string]: React.ComponentType<any> } = {
    "Home": HomeView,
    "Profile": ProfileView,
    "CreateClub": CreateClubView
}

Object.keys(views).forEach(key => {
    config.addView(key, Prelude(views[key]))
});

// Add your context providers here
config.addContextProvider("user", UserContext);
config.addContextProvider("csrf_token", CSRFTokenContext);

const rootElement = document.getElementById("root")!;
const initialResponse = JSON.parse(
    document.getElementById("initial-response")!.textContent!
);

ReactDOM.createRoot(rootElement).render(
    <React.StrictMode>
        <DjangoBridge.App config={config} initialResponse={initialResponse} />
    </React.StrictMode>
);
