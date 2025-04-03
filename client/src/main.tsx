import React from "react";
import ReactDOM from "react-dom/client";
import * as DjangoBridge from "@django-bridge/react";
import { CSRFTokenContext } from "@cafe/hooks/useCSRFToken";
import '@mantine/core/styles.css';
import '@mantine/notifications/styles.css';
import './style.css';

import { UserContext } from "@cafe/hooks/useUser";
import { Prelude } from "./components/Prelude/Prelude";
import { appName, routeMap } from "./routeMap";

const config = new DjangoBridge.Config();


Object.keys(routeMap).forEach(key => {
    config.addView(`${appName}:${key}`, (...props) => {
        const Component = routeMap[key];
        return (
            <Prelude>
                <Component {...props} />
            </Prelude>
        )
    });
});


// Add your context providers here
config.addContextProvider("user", UserContext);
config.addContextProvider("csrf_token", CSRFTokenContext);

const rootElement = document.getElementById("root")!;
const initialResponse = JSON.parse(
    document.getElementById("initial-response")!.textContent!
);

if (!import.meta.env.PROD) {
    console.log("Initial response:", initialResponse);
}


ReactDOM.createRoot(rootElement).render(
    <React.StrictMode>
        <DjangoBridge.App config={config} initialResponse={initialResponse} />
    </React.StrictMode>
);
