import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
// import { analyzer } from 'vite-bundle-analyzer'

// https://vite.dev/config/
export default defineConfig({
  base: "/static/",
  server: {
    cors: true
  },
  build: {
    manifest: true,
    rollupOptions: {
      input: "/src/main.tsx",
    },
  },
  plugins: [
    react(),
    // analyzer()
  ],
  resolve: {
    alias: {
      "@cafe": "/src",
    }
  }
})
