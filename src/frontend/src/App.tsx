import '@shoelace-style/shoelace/dist/themes/light.css';
import { setBasePath } from "@shoelace-style/shoelace/dist/utilities/base-path.js";
import { Route, Switch } from 'wouter-preact';
import { Home } from '@orchard/pages/Home';
import { DiscordCallback } from './pages/DiscordCallback';

setBasePath('https://cdn.jsdelivr.net/npm/@shoelace-style/shoelace@2.9.0/cdn/');

export function App() {

    return (
        <Switch>
            <Route path="/discord_callback"><DiscordCallback /></Route>
            <Route path="/"><Home/></Route>
            <Route>This is rendered when nothing above has matched</Route>
        </Switch>
    );
}
