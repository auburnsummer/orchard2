// Initialize Shoelace: https://shoelace.style/getting-started/installation#bundling
import '@shoelace-style/shoelace/dist/themes/light.css';
import '@shoelace-style/shoelace/dist/themes/dark.css';
import { setBasePath } from '@shoelace-style/shoelace/dist/utilities/base-path.js';
import { registerIconLibrary } from '@shoelace-style/shoelace/dist/utilities/icon-library.js';
import './app.css';
import { authTokenSig } from './signals/auth.js';

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

export function App() {
	return (
		<div>
			<h1>hello!</h1>
			<p>{authTokenSig}</p>
		</div>
	);
}
