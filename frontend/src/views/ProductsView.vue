<template>
  <div class="products-page">
    <HeaderComponent />

    <div class="container page-content">
      <div class="page-header">
        <h1>Nossos Produtos</h1>
        <p>Encontre a peça que você precisa</p>
      </div>

      <!-- Filters -->
      <div class="filters">
        <input
          type="text"
          placeholder="Buscar por nome, marca ou SKU..."
          v-model="searchQuery"
          @input="handleSearchInput"
          class="search-input"
        />

        <div class="filter-buttons">
          <button
            class="filter-btn"
            :class="{ active: !selectedCategory }"
            @click="toggleCategory(null)"
          >
            Todas
          </button>
          <button
            v-for="category in categories"
            :key="category.id"
            class="filter-btn"
            :class="{ active: selectedCategory === category.id }"
            @click="toggleCategory(category.id)"
          >
            {{ category.name }}
          </button>
        </div>
      </div>

      <!-- Products Grid -->
      <ProductGrid
        :products="products"
        :loading="loading"
      />

      <!-- Pagination -->
      <div v-if="pagination.count > 0 && totalPages > 1" class="pagination">
        <button
          class="pagination-btn"
          :disabled="!pagination.previous"
          @click="goToPage(currentPage - 1)"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="15 18 9 12 15 6"></polyline>
          </svg>
          Anterior
        </button>

        <span class="pagination-info">
          Página {{ currentPage }} de {{ totalPages }}
        </span>

        <button
          class="pagination-btn"
          :disabled="!pagination.next"
          @click="goToPage(currentPage + 1)"
        >
          Próxima
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="9 18 15 12 9 6"></polyline>
          </svg>
        </button>
      </div>
    </div>

    <FooterComponent />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useProductsStore } from '../stores/products';
import { useRoute, useRouter } from 'vue-router';
import HeaderComponent from '../components/layout/HeaderComponent.vue';
import FooterComponent from '../components/layout/FooterComponent.vue';
import ProductGrid from '../components/products/ProductGrid.vue';

const productsStore = useProductsStore();
const route = useRoute();
const router = useRouter();

const searchQuery = ref('');
const selectedCategory = ref(null);
const currentPage = ref(1);
const loading = ref(false);

const products = computed(() => productsStore.products);
const categories = computed(() => productsStore.categories);
const pagination = computed(() => productsStore.pagination);
const totalPages = computed(() => Math.ceil(pagination.value.count / 12));

let searchTimeout = null;

const fetchProducts = async () => {
  loading.value = true;

  const params = {
    page: currentPage.value,
    search: searchQuery.value || undefined,
    category: selectedCategory.value || undefined,
  };

  await productsStore.fetchProducts(params);
  loading.value = false;
};

const handleSearchInput = () => {
  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(() => {
    currentPage.value = 1;
    fetchProducts();
  }, 500);
};

const toggleCategory = (categoryId) => {
  selectedCategory.value = categoryId;
  currentPage.value = 1;
  fetchProducts();
};

const goToPage = (page) => {
  if (page < 1 || page > totalPages.value) return;
  currentPage.value = page;
  fetchProducts();
  window.scrollTo({ top: 0, behavior: 'smooth' });
};

onMounted(async () => {
  await productsStore.fetchCategories();

  // Verificar query params
  if (route.query.category) {
    selectedCategory.value = parseInt(route.query.category);
  }
  if (route.query.search) {
    searchQuery.value = route.query.search;
  }

  await fetchProducts();
});

watch([selectedCategory, searchQuery], () => {
  router.push({
    query: {
      ...(selectedCategory.value && { category: selectedCategory.value }),
      ...(searchQuery.value && { search: searchQuery.value }),
    },
  });
});
</script>

<style scoped>
.products-page {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.page-content {
  padding: var(--spacing-3xl) var(--spacing-xl);
  flex: 1;
}

.page-header {
  text-align: center;
  margin-bottom: var(--spacing-3xl);
}

.page-header h1 {
  margin-bottom: var(--spacing-sm);
}

.page-header p {
  color: var(--color-text-secondary);
  font-size: var(--text-lg);
}

.filters {
  margin-bottom: var(--spacing-3xl);
}

.search-input {
  width: 100%;
  padding: var(--spacing-md) var(--spacing-lg);
  background-color: var(--color-bg-card);
  border: 1px solid var(--color-text-muted);
  border-radius: var(--radius-md);
  color: var(--color-text-primary);
  font-size: var(--text-base);
  margin-bottom: var(--spacing-lg);
}

.filter-buttons {
  display: flex;
  gap: var(--spacing-sm);
  flex-wrap: wrap;
}

.filter-btn {
  padding: var(--spacing-sm) var(--spacing-lg);
  background-color: var(--color-bg-card);
  border: 1px solid var(--color-text-muted);
  border-radius: var(--radius-full);
  color: var(--color-text-primary);
  font-size: var(--text-sm);
  font-weight: var(--font-semibold);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.filter-btn:hover {
  border-color: var(--color-primary);
  color: var(--color-primary);
}

.filter-btn.active {
  background-color: var(--color-primary);
  border-color: var(--color-primary);
  color: var(--color-bg-primary);
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: var(--spacing-xl);
  margin-top: var(--spacing-3xl);
}

.pagination-btn {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-md) var(--spacing-lg);
  background-color: var(--color-bg-card);
  border: none;
  border-radius: var(--radius-md);
  color: var(--color-text-primary);
  font-size: var(--text-base);
  font-weight: var(--font-semibold);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.pagination-btn:hover:not(:disabled) {
  background-color: var(--color-primary);
  color: var(--color-bg-primary);
  transform: translateY(-2px);
}

.pagination-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.pagination-info {
  color: var(--color-text-secondary);
  font-size: var(--text-base);
  font-weight: var(--font-medium);
}
</style>
