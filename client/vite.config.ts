import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";
// import { analyzer } from 'vite-bundle-analyzer'

// https://vite.dev/config/
export default defineConfig({
  base: "/static/",
  server: {
    cors: true,
  },
  build: {
    manifest: true,
    rollupOptions: {
      input: "/src/main.tsx",
      output: {
        manualChunks: function(id) {
          if (id.includes('node_modules')) {
            return 'vendor';
          }

          return null;
        }
      }
    },
  },
  plugins: [
    react(),
    tailwindcss(),
    // analyzer()
  ],
  resolve: {
    alias: {
      "@cafe": "/src",
    },
  },
});
