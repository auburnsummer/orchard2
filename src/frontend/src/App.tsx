import '@shoelace-style/shoelace/dist/themes/light.css';
import '@shoelace-style/shoelace/dist/themes/dark.css';
import { setBasePath } from "@shoelace-style/shoelace/dist/utilities/base-path.js";
import { Route, Switch } from 'wouter-preact';
import { Home } from '@orchard/pages/Home';
import { DiscordCallback } from './pages/DiscordCallback';
import { PublisherDiscordRegister } from './pages/PublisherDiscordRegister';
import { NotFound } from './pages/404';
import { PublisherAdd } from './pages/PublisherAdd';
import { Button, TagInput } from './ui';
import { useState } from 'preact/hooks';

setBasePath('https://cdn.jsdelivr.net/npm/@shoelace-style/shoelace@2.9.0/cdn/');

function Scaffold() {
    const [items, setItems] = useState(["hello", "world", "hello"])

    const validationMessage = items.length ? "" : "There needs to be at least one thingo."

    return (
        <form style={{padding: "3rem"}}>
            <TagInput items={items} onItems={setItems} commaSubmits validationMessage={validationMessage} inputProps={{"label": "Tag test"}}/>
            <Button type="submit">Submit</Button>
        </form>
    )
}

export function App() {

    return (
        <Switch>
            <Route path="/scaffold"><Scaffold/></Route>
            <Route path="/publisher/add"><PublisherAdd /></Route>
            <Route path="/publisher/discord_register"><PublisherDiscordRegister /></Route>
            <Route path="/discord_callback"><DiscordCallback /></Route>
            <Route path="/"><Home/></Route>
            <Route><NotFound /></Route>
        </Switch>
    );
}
