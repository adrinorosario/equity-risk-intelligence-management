/**
 * TLDR; Vite configuration for React frontend.
 * TODO: Add proxy config for backend, env var typing, and build optimizations.
 */

import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173
  }
});

