import { defineConfig } from 'vite';
import { svelte } from "@sveltejs/vite-plugin-svelte";

export default defineConfig({
	plugins: [svelte()],
	test: {
    environment: 'jsdom',
		setupFiles: ['./vitest.setup.js'],
  },
	// Tell Vitest to use the `browser` entry points in `package.json` files, even though it's running in Node
	resolve: process.env.VITEST
		? {
				conditions: ['browser']
			}
		: undefined
});