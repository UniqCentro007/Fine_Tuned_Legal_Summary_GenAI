import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,   // Your dev server port
    cors: true    // Allow CORS so it can connect to FastAPI
  }
});