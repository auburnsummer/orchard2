// Initialize Shoelace: https://shoelace.style/getting-started/installation#bundling
import '@shoelace-style/shoelace/dist/themes/light.css';
import '@shoelace-style/shoelace/dist/themes/dark.css';
import { setBasePath } from '@shoelace-style/shoelace/dist/utilities/base-path.js';
import { registerIconLibrary } from '@shoelace-style/shoelace/dist/utilities/icon-library.js';
import { Route, Switch } from 'wouter-preact';
import './App.css';
import { NotFound } from './pages/404';
import { PublisherDiscordRegister } from './pages/PublisherDiscordRegister';
import { PublisherAdd } from './pages/PublisherAdd';
import { registerPopStateHandler } from './signals/handlePopState';
import { DiscordCallback } from '~/pages/DiscordCallback';
import { Home } from '~/pages/Home';

setBasePath('https://cdn.jsdelivr.net/npm/@shoelace-style/shoelace@2.12.0/cdn/');

// https://shoelace.style/components/icon/#font-awesome
registerIconLibrary('fa', {
	resolver(name) {
		const filename = name.replace(/^fa[rbs]-/, '');
		let folder = 'regular';
		if (name.startsWith('fas-')) {
			folder = 'solid';
		}

		if (name.startsWith('fab-')) {
			folder = 'brands';
		}

		return `https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.4.2/svgs/${folder}/${filename}.svg`;
	},
	mutator(svg) {
		svg.setAttribute('fill', 'currentColor');
	},
});

registerPopStateHandler();

export function App() {
	return (
		<Switch>
			<Route path='/publisher/add/rd'><PublisherAdd /></Route>
			<Route path='/discord_callback'><DiscordCallback /></Route>
			<Route path='/publisher/discord_register'><PublisherDiscordRegister /></Route>
			<Route path='/'><Home/></Route>
			<Route><NotFound /></Route>
		</Switch>
	);
}
