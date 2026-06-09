import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Attach JWT token to every request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Handle token expiry
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// ─── Auth APIs ────────────────────────────────────────────────
export const authAPI = {
  register: (data) => api.post('/api/auth/register', data),
  login:    (data) => api.post('/api/auth/login', data),
  me:       ()     => api.get('/api/auth/me'),
}

// ─── Campaign APIs ────────────────────────────────────────────
export const campaignAPI = {
  list:       (params) => api.get('/api/campaigns/', { params }),
  getMine:    ()       => api.get('/api/campaigns/brand/my-campaigns'),
  getById:    (id)     => api.get(`/api/campaigns/${id}`),
  create:     (data)   => api.post('/api/campaigns/', data),
  update:     (id, data) => api.put(`/api/campaigns/${id}`, data),
  delete:     (id)     => api.delete(`/api/campaigns/${id}`),
}

// ─── Application APIs ─────────────────────────────────────────
export const applicationAPI = {
  apply:          (campaignId, data) => api.post(`/api/applications/campaign/${campaignId}`, data),
  getMine:        ()                 => api.get('/api/applications/my-applications'),
  getCampaignApps: (campaignId)      => api.get(`/api/applications/campaign/${campaignId}`),
  approve:        (id)               => api.put(`/api/applications/${id}/approve`),
  reject:         (id)               => api.put(`/api/applications/${id}/reject`),
}

// ─── Deliverable APIs ─────────────────────────────────────────
export const deliverableAPI = {
  submit:    (campaignId, formData) => api.post(
    `/api/deliverables/campaign/${campaignId}`,
    formData,
    { headers: { 'Content-Type': 'multipart/form-data' } }
  ),
  getMine:   ()         => api.get('/api/deliverables/my-deliverables'),
  getCampaign: (id)     => api.get(`/api/deliverables/campaign/${id}`),
  approve:   (id)       => api.put(`/api/deliverables/${id}/approve`),
  reject:    (id)       => api.put(`/api/deliverables/${id}/reject`),
}

// ─── Payment APIs ─────────────────────────────────────────────
export const paymentAPI = {
  createIntent: (data) => api.post('/api/payments/create-intent', data),
  release:      (id)   => api.put(`/api/payments/${id}/release`),
  getMine:      ()     => api.get('/api/payments/my-earnings'),
  getCampaign:  (id)   => api.get(`/api/payments/campaign/${id}`),
}

// ─── Analytics APIs ───────────────────────────────────────────
export const analyticsAPI = {
  brandDashboard:      () => api.get('/api/analytics/brand/dashboard'),
  campaignPerformance: () => api.get('/api/analytics/brand/campaign-performance'),
  influencerDashboard: () => api.get('/api/analytics/influencer/dashboard'),
}

// ─── User APIs ────────────────────────────────────────────────
export const userAPI = {
  updateProfile:    (data)     => api.put('/api/users/me', data),
  getProfile:       ()         => api.get('/api/users/influencer/profile'),
  updateInfluencer: (data)     => api.put('/api/users/influencer/profile', data),
  uploadPortfolio:  (formData) => api.post(
    '/api/users/influencer/upload/portfolio',
    formData,
    { headers: { 'Content-Type': 'multipart/form-data' } }
  ),
  uploadMediaKit: (formData) => api.post(
    '/api/users/influencer/upload/media-kit',
    formData,
    { headers: { 'Content-Type': 'multipart/form-data' } }
  ),
}

export default api