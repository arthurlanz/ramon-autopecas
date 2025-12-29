import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para adicionar token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Interceptor para refresh token
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        const { data } = await axios.post(`${API_BASE_URL}/auth/refresh/`, {
          refresh: refreshToken,
        });

        localStorage.setItem('access_token', data.access);
        api.defaults.headers.Authorization = `Bearer ${data.access}`;
        originalRequest.headers.Authorization = `Bearer ${data.access}`;

        return api(originalRequest);
      } catch (refreshError) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default api;

// Auth
export const authAPI = {
  login: (credentials) => api.post('/auth/login/', credentials),
  register: (userData) => api.post('/users/', userData),
  getMe: () => api.get('/users/me/'),
  refreshToken: (refresh) => api.post('/auth/refresh/', { refresh }),
};

// Products
export const productsAPI = {
  getAll: (params) => api.get('/products/', { params }),
  getOne: (slug) => api.get(`/products/${slug}/`),
  getFeatured: () => api.get('/products/featured/'),
  getLowStock: () => api.get('/products/low_stock/'),
  getStatistics: () => api.get('/products/statistics/'),
  create: (formData) => api.post('/products/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  }),
  update: (slug, formData) => api.put(`/products/${slug}/`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  }),
  delete: (slug) => api.delete(`/products/${slug}/`),
  syncToML: (slug) => api.post(`/products/${slug}/sync_to_ml/`),
};

// Categories
export const categoriesAPI = {
  getAll: () => api.get('/categories/'),
  getOne: (slug) => api.get(`/categories/${slug}/`),
};

// Orders
export const ordersAPI = {
  getAll: (params) => api.get('/orders/', { params }),
  getOne: (id) => api.get(`/orders/${id}/`),
  create: (orderData) => api.post('/orders/', orderData),
  updateStatus: (id, status) => api.post(`/orders/${id}/update_status/`, { status }),
  addTracking: (id, trackingData) => api.post(`/orders/${id}/add_tracking/`, trackingData),
  getStatistics: () => api.get('/orders/statistics/'),
};

// Dashboard
export const dashboardAPI = {
  getOverview: () => api.get('/dashboard/overview/'),
  getSalesChart: (days = 30) => api.get('/dashboard/sales_chart/', { params: { days } }),
  getRevenueByCategory: () => api.get('/dashboard/revenue_by_category/'),
  getRecentOrders: (limit = 10) => api.get('/dashboard/recent_orders/', { params: { limit } }),
  getAlerts: () => api.get('/dashboard/alerts/'),
};

// Mercado Livre
export const mlAPI = {
  authorize: () => api.get('/ml/authorize/'),
  getSyncLogs: (params) => api.get('/ml-logs/', { params }),
};
