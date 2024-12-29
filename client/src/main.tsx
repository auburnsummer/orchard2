import React from "react";
import ReactDOM from "react-dom/client";
import * as DjangoBridge from "@django-bridge/react";
import { CSRFTokenContext } from "./contexts";
import HomeView from "./views/HomeView";
import '@mantine/core/styles.css';

import { MantineProvider } from '@mantine/core';

const config = new DjangoBridge.Config();

// Add your views here
config.addView("Home", HomeView);

// Add your context providers here
config.addContextProvider("csrf_token", CSRFTokenContext);

const rootElement = document.getElementById("root")!;
const initialResponse = JSON.parse(
    document.getElementById("initial-response")!.textContent!
);

ReactDOM.createRoot(rootElement).render(
    <React.StrictMode>
        <MantineProvider>
            <DjangoBridge.App config={config} initialResponse={initialResponse} />
        </MantineProvider>
    </React.StrictMode>
);
