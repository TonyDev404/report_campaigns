import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'

// https://vite.dev/config/
export default defineConfig({
  plugins: [svelte()],
  server: {
    host: "127.0.0.1",
    proxy: {
      "/campaigns": {
        target: "http://127.0.0.1:8000",
        changeOrigin: true,
      },
    },
  },
});
