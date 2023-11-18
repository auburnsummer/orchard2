import '@shoelace-style/shoelace/dist/themes/light.css';
import '@shoelace-style/shoelace/dist/themes/dark.css';
import { setBasePath } from "@shoelace-style/shoelace/dist/utilities/base-path.js";
import { Route, Switch } from 'wouter-preact';
import { Home } from '@orchard/pages/Home';
import { DiscordCallback } from './pages/DiscordCallback';
import { PublisherDiscordRegister } from './pages/PublisherDiscordRegister';
import { NotFound } from './pages/404';
import { PublisherAdd } from './pages/PublisherAdd';
import { registerIconLibrary } from '@shoelace-style/shoelace/dist/utilities/icon-library.js';

setBasePath('https://cdn.jsdelivr.net/npm/@shoelace-style/shoelace@2.9.0/cdn/');


registerIconLibrary('fa', {
  resolver: name => {
    const filename = name.replace(/^fa[rbs]-/, '');
    let folder = 'regular';
    if (name.substring(0, 4) === 'fas-') folder = 'solid';
    if (name.substring(0, 4) === 'fab-') folder = 'brands';
    return `https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.4.2/svgs/${folder}/${filename}.svg`;
  },
  mutator: svg => svg.setAttribute('fill', 'currentColor')
});



export function App() {
    return (
        <Switch>
            <Route path="/publisher/add/rd"><PublisherAdd /></Route>
            <Route path="/publisher/discord_register"><PublisherDiscordRegister /></Route>
            <Route path="/discord_callback"><DiscordCallback /></Route>
            <Route path="/"><Home/></Route>
            <Route><NotFound /></Route>
        </Switch>
    );
}
