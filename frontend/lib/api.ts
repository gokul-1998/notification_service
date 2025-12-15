import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
});

// Add token to requests
api.interceptors.request.use((config) => {
  if (typeof window !== 'undefined') {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;
});

// Auth API
export const authAPI = {
  register: (data: { username: string; email: string; password: string; is_admin?: boolean }) =>
    api.post('/api/auth/register', data),
  
  login: async (username: string, password: string) => {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
    return api.post('/api/auth/login', formData);
  },
};

// Notifications API
export const notificationsAPI = {
  create: (data: { title: string; message: string }) =>
    api.post('/api/notifications/', data),
  
  getAll: (unread_only: boolean = false) =>
    api.get('/api/notifications/', { params: { unread_only } }),
  
  getUnreadCount: () =>
    api.get('/api/notifications/unread-count'),
  
  markAsRead: (id: number) =>
    api.put(`/api/notifications/${id}/read`),
  
  markAllAsRead: () =>
    api.put('/api/notifications/mark-all-read'),
  
  delete: (id: number) =>
    api.delete(`/api/notifications/${id}`),
};

export default api;
