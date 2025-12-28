import axios from 'axios'

const API_BASE_URL = '/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const fetchUsers = async () => {
  const response = await api.get('/users')
  return response.data
}

export const fetchDocuments = async () => {
  const response = await api.get('/documents')
  return response.data
}

export const fetchPermissions = async (role) => {
  const response = await api.get(`/permissions/${role}`)
  return response.data
}

export const sendAgentQuery = async (user, query) => {
  const response = await api.post('/agent/query', {
    user,
    query
  })
  return response.data
}

export default api
