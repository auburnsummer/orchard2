import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";
// import { analyzer } from 'vite-bundle-analyzer'

const isPrBuild = process.env.VITE_PR_BUILD === "true";

// https://vite.dev/config/
export default defineConfig(() => ({
  base: isPrBuild ? "./" : "/static/",
  server: {
    cors: true,
    origin: "http://localhost:5173",
  },
  build: {
    manifest: true,
    rollupOptions: {
      input: "/src/main.tsx",
      output: {
        ...(isPrBuild && {
          entryFileNames: "[name].js",
          chunkFileNames: "[name].js",
          assetFileNames: "[name][extname]",
        }),
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
}));
