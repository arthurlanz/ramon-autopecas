import { defineStore } from 'pinia';
import { dashboardAPI } from '../services/api';

export const useDashboardStore = defineStore('dashboard', {
  state: () => ({
    overview: null,
    salesChart: [],
    revenueByCategory: [],
    recentOrders: [],
    alerts: [],
    loading: false,
    error: null,
  }),

  actions: {
    async fetchOverview() {
      this.loading = true;
      try {
        const { data } = await dashboardAPI.getOverview();
        this.overview = data;
      } catch (error) {
        this.error = error.response?.data?.detail || 'Erro ao carregar overview';
        console.error('Fetch overview error:', error);
      } finally {
        this.loading = false;
      }
    },

    async fetchSalesChart(days = 30) {
      try {
        const { data } = await dashboardAPI.getSalesChart(days);
        this.salesChart = data;
      } catch (error) {
        console.error('Fetch sales chart error:', error);
      }
    },

    async fetchRevenueByCategory() {
      try {
        const { data } = await dashboardAPI.getRevenueByCategory();
        this.revenueByCategory = data;
      } catch (error) {
        console.error('Fetch revenue by category error:', error);
      }
    },

    async fetchRecentOrders(limit = 10) {
      try {
        const { data } = await dashboardAPI.getRecentOrders(limit);
        this.recentOrders = data;
      } catch (error) {
        console.error('Fetch recent orders error:', error);
      }
    },

    async fetchAlerts() {
      try {
        const { data } = await dashboardAPI.getAlerts();
        this.alerts = data;
      } catch (error) {
        console.error('Fetch alerts error:', error);
      }
    },

    async fetchAll() {
      await Promise.all([
        this.fetchOverview(),
        this.fetchSalesChart(),
        this.fetchRevenueByCategory(),
        this.fetchRecentOrders(),
        this.fetchAlerts(),
      ]);
    },
  },
});
