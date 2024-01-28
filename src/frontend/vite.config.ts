import * as path from 'node:path';
import { fileURLToPath } from 'node:url';
import { defineConfig } from 'vite';
import preact from '@preact/preset-vite';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
// https://vitejs.dev/config/
export default defineConfig({
	plugins: [preact()],
	resolve: {
		alias: {
			// eslint-disable-next-line @typescript-eslint/naming-convention
			'~': path.resolve(__dirname, './src'),
		},
	},
});
