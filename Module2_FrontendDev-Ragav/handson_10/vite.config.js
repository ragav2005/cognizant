import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { mockCourses } from './src/api/mockCatalog.js'

export default defineConfig({
  plugins: [
    vue(),
    {
      // Mock REST endpoints so the central API layer can be exercised in dev
      name: 'mock-api',
      configureServer(server) {
        server.middlewares.use('/api/courses', (req, res, next) => {
          if (req.method === 'GET') {
            res.setHeader('Content-Type', 'application/json')
            res.end(JSON.stringify(mockCourses))
            return
          }
          next()
        })
      },
    },
  ],
})