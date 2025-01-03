import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  base: "/static/",
  build: {
    manifest: true,
    rollupOptions: {
      input: "/src/main.tsx",
    },
  },
  plugins: [react()],
  resolve: {
    alias: {
      "@cafe": "/src",
    }
  }
})
