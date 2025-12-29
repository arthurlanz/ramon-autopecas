<template>
  <router-link
    :to="`/produtos?category=${category.id}`"
    class="category-card"
  >
    <div class="category-icon">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="40"
        height="40"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        v-html="iconPath"
      ></svg>
    </div>
    <h3 class="category-name">{{ category.name }}</h3>
    <p class="category-count">{{ category.product_count }} produtos</p>
  </router-link>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  category: {
    type: Object,
    required: true,
  },
});

const iconPath = computed(() => {
  const icons = {
    Freios: '<circle cx="12" cy="12" r="10"></circle><circle cx="12" cy="12" r="6"></circle><circle cx="12" cy="12" r="2"></circle>',
    Motor: '<circle cx="12" cy="12" r="3"></circle><path d="M12 1v6m0 6v6m5.2-13.2l-4.2 4.2m0 6l4.2 4.2M1 12h6m6 0h6m-13.2-5.2l4.2 4.2m0 6l-4.2 4.2"></path>',
    Suspensão: '<line x1="12" y1="2" x2="12" y2="6"></line><line x1="12" y1="18" x2="12" y2="22"></line><line x1="4.93" y1="4.93" x2="7.76" y2="7.76"></line><line x1="16.24" y1="16.24" x2="19.07" y2="19.07"></line><line x1="2" y1="12" x2="6" y2="12"></line><line x1="18" y1="12" x2="22" y2="12"></line><line x1="4.93" y1="19.07" x2="7.76" y2="16.24"></line><line x1="16.24" y1="7.76" x2="19.07" y2="4.93"></line>',
    Elétrica: '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon>',
    Filtros: '<polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon>',
    Escapamento: '<path d="M4 12h16M4 6h16M4 18h16"></path>',
  };

  return icons[props.category.name] || icons.Freios;
});
</script>

<style scoped>
.category-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: var(--spacing-2xl);
  background-color: var(--color-bg-card);
  border-radius: var(--radius-xl);
  transition: all var(--transition-base);
  text-align: center;
}

.category-card:hover {
  transform: translateY(-8px);
  box-shadow: var(--shadow-xl);
  background-color: var(--color-bg-card-hover);
}

.category-icon {
  width: 80px;
  height: 80px;
  border-radius: var(--radius-full);
  background-color: rgba(253, 184, 19, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: var(--spacing-lg);
  transition: all var(--transition-base);
}

.category-card:hover .category-icon {
  background-color: var(--color-primary);
  transform: scale(1.1);
}

.category-icon svg {
  color: var(--color-primary);
  transition: color var(--transition-base);
}

.category-card:hover .category-icon svg {
  color: var(--color-bg-primary);
}

.category-name {
  font-size: var(--text-xl);
  font-weight: var(--font-black);
  color: var(--color-text-primary);
  text-transform: uppercase;
  margin-bottom: var(--spacing-xs);
}

.category-count {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  margin: 0;
}
</style>
