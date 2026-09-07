import axios from 'axios';

// Default to relative paths for single-domain production Cloud Run deployment (annapoorniacademy.com)
// If VITE_API_BASE_URL is explicitly set during dev/external hosting, it will use that base URL.
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '';

const API = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Interceptor to attach Admin JWT token to protected requests
API.interceptors.request.use((config) => {
  const token = localStorage.getItem('admin_token');
  if (token && config.url && config.url.includes('/api/admin')) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});

// Response Interceptor for global auth error handling
API.interceptors.response.use((response) => response, (error) => {
  if (error.response && error.response.status === 401 && window.location.pathname.startsWith('/admin') && !window.location.pathname.includes('/login')) {
    localStorage.removeItem('admin_token');
    localStorage.removeItem('admin_user');
    window.location.href = '/admin/login';
  }
  return Promise.reject(error);
});

export default API;
