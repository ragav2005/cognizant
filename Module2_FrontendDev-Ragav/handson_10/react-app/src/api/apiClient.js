import axios from 'axios'

const apiClient = axios.create({
  baseURL: 'https://jsonplaceholder.typicode.com',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

apiClient.interceptors.request.use((config) => {
  const mockToken = 'mock-jwt-token-12345'
  if (mockToken) config.headers.Authorization = `Bearer ${mockToken}`
  return config
})

apiClient.interceptors.response.use(
  (response) => response.data,
  (error) => {
    const statusCode = error.response?.status ?? 0
    const message = error.response?.data?.message ?? error.message ?? 'Unknown error'
    const standardizedError = new Error(message)
    standardizedError.statusCode = statusCode
    return Promise.reject(standardizedError)
  }
)

export default apiClient
