import '@shoelace-style/shoelace/dist/themes/light.css';
import { setBasePath } from "@shoelace-style/shoelace/dist/utilities/base-path.js";
import { Route, Switch } from 'wouter-preact';
import { Home } from '@orchard/pages/Home';

setBasePath('https://cdn.jsdelivr.net/npm/@shoelace-style/shoelace@2.9.0/cdn/');

export function App() {

    return (
        <Switch>
            <Route path="/"><Home/></Route>
            <Route>This is rendered when nothing above has matched</Route>
        </Switch>
    );
}
