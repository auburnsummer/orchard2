if (import.meta.env.MODE ==='development') {
    import("preact/debug");
}
  

import { render } from "preact";
import { App } from "./App";

import "./main.css";

render(<App />, document.querySelector("#app")!);
