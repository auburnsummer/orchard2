if (import.meta.env.MODE === 'development') {
	import('preact/debug');
}

import {render} from 'preact';
import {App} from './App';

render(<App />, document.querySelector('#root')!);
