import React from "react";
import ReactDOM from "react-dom/client";
import { CSRFTokenContext } from "@cafe/hooks/useCSRFToken";
import "./style.css";

import { UserContext } from "@cafe/hooks/useUser";
import { Prelude } from "./components/Prelude/Prelude";
import { routeMap } from "./routeMap";
import { App as MinibridgeApp } from "./minibridge";
import { Outlet } from "./minibridge/components/Outlet";
import { Config } from "./minibridge/config";

const config: Config = {
  views: routeMap,
  contextProviders: {
    user: UserContext,
    csrf_token: CSRFTokenContext,
  },
};

const rootElement = document.getElementById("root")!;
const initialResponse = JSON.parse(
  document.getElementById("initial-response")!.textContent!,
);

if (!import.meta.env.PROD) {
  console.log("Initial response:", initialResponse);
}

ReactDOM.createRoot(rootElement).render(
  <React.StrictMode>
    <MinibridgeApp config={config} initialResponse={initialResponse}>
      <Prelude>
        <Outlet />
      </Prelude>
    </MinibridgeApp>
  </React.StrictMode>,
);
