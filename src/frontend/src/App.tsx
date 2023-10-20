import '@shoelace-style/shoelace/dist/themes/light.css';
import '@shoelace-style/shoelace/dist/themes/dark.css';
import { setBasePath } from "@shoelace-style/shoelace/dist/utilities/base-path.js";
import { Route, Switch } from 'wouter-preact';
import { Home } from '@orchard/pages/Home';
import { DiscordCallback } from './pages/DiscordCallback';
import { PublisherDiscordRegister } from './pages/PublisherDiscordRegister';
import { NotFound } from './pages/404';

setBasePath('https://cdn.jsdelivr.net/npm/@shoelace-style/shoelace@2.9.0/cdn/');

export function App() {

    return (
        <Switch>
            <Route path="/publisher/discord_register"><PublisherDiscordRegister /></Route>
            <Route path="/discord_callback"><DiscordCallback /></Route>
            <Route path="/"><Home/></Route>
            <Route><NotFound /></Route>
        </Switch>
    );
}
