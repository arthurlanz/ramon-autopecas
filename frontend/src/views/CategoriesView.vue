<template>
  <div class="categories-page">
    <HeaderComponent />

    <div class="container page-content">
      <div class="page-header">
        <h1>Categorias</h1>
        <p>Navegue por nossas categorias de produtos</p>
      </div>

      <div v-if="loading" class="loading-container">
        <div class="loading"></div>
        <p>Carregando categorias...</p>
      </div>

      <div v-else class="categories-grid">
        <CategoryCard
          v-for="category in categories"
          :key="category.id"
          :category="category"
        />
      </div>
    </div>

    <FooterComponent />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useProductsStore } from '../stores/products';
import HeaderComponent from '../components/layout/HeaderComponent.vue';
import FooterComponent from '../components/layout/FooterComponent.vue';
import CategoryCard from '../components/products/CategoryCard.vue';

const productsStore = useProductsStore();
const categories = ref([]);
const loading = ref(false);

onMounted(async () => {
  loading.value = true;
  await productsStore.fetchCategories();
  categories.value = productsStore.categories;
  loading.value = false;
});
</script>

<style scoped>
.categories-page {
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

.categories-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: var(--spacing-xl);
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 50vh;
  gap: var(--spacing-lg);
}

@media (max-width: 640px) {
  .categories-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
