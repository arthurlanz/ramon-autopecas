<template>
  <div class="product-grid">
    <ProductCard
      v-for="product in products"
      :key="product.id"
      :product="product"
      :show-view-button="showViewButton"
      @buy="handleBuy"
    />
  </div>

  <div v-if="loading" class="loading-container">
    <div class="loading"></div>
    <p>Carregando produtos...</p>
  </div>

  <div v-if="!loading && products.length === 0" class="empty-state">
    <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <circle cx="12" cy="12" r="10"></circle>
      <line x1="12" y1="8" x2="12" y2="12"></line>
      <line x1="12" y1="16" x2="12.01" y2="16"></line>
    </svg>
    <h3>Nenhum produto encontrado</h3>
    <p>Tente ajustar os filtros ou volte mais tarde.</p>
  </div>
</template>

<script setup>
import ProductCard from './ProductCard.vue';

defineProps({
  products: {
    type: Array,
    default: () => [],
  },
  loading: {
    type: Boolean,
    default: false,
  },
  showViewButton: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(['buy']);

const handleBuy = (product) => {
  emit('buy', product);
};
</script>

<style scoped>
.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: var(--spacing-xl);
  margin-bottom: var(--spacing-2xl);
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-3xl);
  gap: var(--spacing-lg);
}

.loading-container p {
  color: var(--color-text-secondary);
  font-size: var(--text-lg);
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-3xl);
  text-align: center;
}

.empty-state svg {
  color: var(--color-text-muted);
  margin-bottom: var(--spacing-lg);
}

.empty-state h3 {
  font-size: var(--text-2xl);
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-sm);
}

.empty-state p {
  color: var(--color-text-secondary);
  font-size: var(--text-base);
}

@media (max-width: 640px) {
  .product-grid {
    grid-template-columns: 1fr;
  }
}
</style>
