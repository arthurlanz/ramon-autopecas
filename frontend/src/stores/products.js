import { defineStore } from 'pinia';
import { productsAPI, categoriesAPI } from '../services/api';

export const useProductsStore = defineStore('products', {
  state: () => ({
    products: [],
    featuredProducts: [],
    product: null,
    categories: [],
    loading: false,
    error: null,
    pagination: {
      count: 0,
      next: null,
      previous: null,
    },
  }),

  actions: {
    async fetchProducts(params = {}) {
      this.loading = true;
      this.error = null;

      try {
        const { data } = await productsAPI.getAll(params);
        this.products = data.results;
        this.pagination = {
          count: data.count,
          next: data.next,
          previous: data.previous,
        };
      } catch (error) {
        this.error = error.response?.data?.detail || 'Erro ao carregar produtos';
        console.error('Fetch products error:', error);
      } finally {
        this.loading = false;
      }
    },

    async fetchFeaturedProducts() {
      try {
        const { data } = await productsAPI.getFeatured();
        this.featuredProducts = data;
      } catch (error) {
        console.error('Fetch featured products error:', error);
      }
    },

    async fetchProduct(slug) {
      this.loading = true;
      this.error = null;

      try {
        const { data } = await productsAPI.getOne(slug);
        this.product = data;
        return data;
      } catch (error) {
        this.error = error.response?.data?.detail || 'Erro ao carregar produto';
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async fetchCategories() {
      try {
        const { data } = await categoriesAPI.getAll();
        this.categories = data.results || data;
      } catch (error) {
        console.error('Fetch categories error:', error);
      }
    },

    async createProduct(formData) {
      this.loading = true;
      this.error = null;

      try {
        const { data } = await productsAPI.create(formData);
        return { success: true, data };
      } catch (error) {
        this.error = error.response?.data || 'Erro ao criar produto';
        return { success: false, error: this.error };
      } finally {
        this.loading = false;
      }
    },

    async updateProduct(slug, formData) {
      this.loading = true;
      this.error = null;

      try {
        const { data } = await productsAPI.update(slug, formData);
        return { success: true, data };
      } catch (error) {
        this.error = error.response?.data || 'Erro ao atualizar produto';
        return { success: false, error: this.error };
      } finally {
        this.loading = false;
      }
    },

    async deleteProduct(slug) {
      try {
        await productsAPI.delete(slug);
        this.products = this.products.filter((p) => p.slug !== slug);
        return { success: true };
      } catch (error) {
        return { success: false, error: error.response?.data };
      }
    },

    async syncProductToML(slug) {
      try {
        const { data } = await productsAPI.syncToML(slug);
        return { success: true, data };
      } catch (error) {
        return { success: false, error: error.response?.data };
      }
    },
  },
});
