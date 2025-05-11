import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [
    react(),              // enable React Fast Refresh & JSX
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
    },
  },
  server: {
    host: '0.0.0.0',      // bind to all interfaces (inside Docker)
    port: 5173,
    proxy: {
      // proxy /api/* to your FastAPI backend
      '/api': {
        // from inside the container, use host.docker.internal to reach your host machine
        // or, if using docker-compose with service name "backend", use http://backend:8000
        target: 'http://host.docker.internal:8000',
        changeOrigin: true,
        secure: false,
      },
    },
  },
})
