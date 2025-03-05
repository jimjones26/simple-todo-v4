import { defineConfig } from 'vite';
import { svelte } from '@sveltejs/vite-plugin-svelte';

export default defineConfig({
  plugins: [svelte()],
  test: {
    globals: true,              // Enables global test functions like describe, it, expect
    environment: 'jsdom',       // Simulates a browser DOM for Svelte components
    setupFiles: ['./vitest.setup.js'], // Path to a setup file (we’ll create this next)
  },
});