import React from "react";
import ReactDOM from "react-dom/client";
import * as DjangoBridge from "@django-bridge/react";
import { CSRFTokenContext } from "@cafe/hooks/useCSRFToken";
import '@mantine/core/styles.css';
import '@mantine/notifications/styles.css';
import './style.css';

import { UserContext } from "@cafe/hooks/useUser";
import { Prelude } from "./components/Prelude/Prelude";
import { routeMap } from "./routeMap";

const config = new DjangoBridge.Config();

Object.keys(routeMap).forEach(key => {
    config.addView(key, routeMap[key])
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
        <DjangoBridge.App config={config} initialResponse={initialResponse}>
            <Prelude>
                <DjangoBridge.Outlet />
            </Prelude>
        </DjangoBridge.App>
    </React.StrictMode>
);
