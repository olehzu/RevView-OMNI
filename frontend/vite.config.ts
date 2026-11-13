import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    // The development server forwards the API to the Application (design/rev.md),
    // so the backend needs no CORS.
    proxy: {
      "/api": "http://127.0.0.1:8000",
    },
  },
});
