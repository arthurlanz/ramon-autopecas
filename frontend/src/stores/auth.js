import { defineStore } from 'pinia';
import { authAPI } from '../services/api';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    isAuthenticated: false,
    loading: false,
    error: null,
  }),

  getters: {
    isOwner: (state) => state.user?.role === 'owner',
    isAdvertiser: (state) => state.user?.role === 'advertiser',
    isCustomer: (state) => state.user?.role === 'customer',
    userRole: (state) => state.user?.role || null,
  },

  actions: {
    async login(username, password) {
      this.loading = true;
      this.error = null;

      try {
        const { data } = await authAPI.login({ username, password });

        localStorage.setItem('access_token', data.access);
        localStorage.setItem('refresh_token', data.refresh);

        await this.fetchUser();

        return { success: true };
      } catch (error) {
        this.error = error.response?.data?.detail || 'Erro ao fazer login';
        return { success: false, message: this.error };
      } finally {
        this.loading = false;
      }
    },

    async register(userData) {
      this.loading = true;
      this.error = null;

      try {
        await authAPI.register(userData);
        return { success: true };
      } catch (error) {
        this.error = error.response?.data || 'Erro ao registrar';
        return { success: false, errors: this.error };
      } finally {
        this.loading = false;
      }
    },

    async fetchUser() {
      try {
        const { data } = await authAPI.getMe();
        this.user = data;
        this.isAuthenticated = true;
      } catch (error) {
        this.logout();
        throw error;
      }
    },

    logout() {
      this.user = null;
      this.isAuthenticated = false;
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
    },

    initializeAuth() {
      const token = localStorage.getItem('access_token');
      if (token) {
        this.fetchUser().catch(() => this.logout());
      }
    },
  },
});
