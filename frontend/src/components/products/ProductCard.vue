<template>
  <div class="product-card">
    <!-- Discount Badge -->
    <div v-if="discount" class="discount-badge">{{ discount }}</div>

    <!-- Product Image -->
    <div class="product-image">
      <img
        :src="product.image || '/placeholder-product.png'"
        :alt="product.title"
      />
    </div>

    <!-- Product Info -->
    <div class="product-info">
      <!-- Category Badge -->
      <span class="category-badge" :style="{ backgroundColor: categoryColor }">
        {{ product.category_name || 'Produto' }}
      </span>

      <!-- Status Badge -->
      <span
        v-if="product.ml_status"
        class="status-badge"
        :class="`status-${product.ml_status}`"
      >
        {{ statusLabel }}
      </span>

      <!-- Title -->
      <h3 class="product-title">{{ product.title }}</h3>

      <!-- Brand and SKU -->
      <p class="product-meta">
        {{ product.brand }} | SKU: {{ product.sku }}
      </p>

      <!-- Price -->
      <div class="product-price">
        <span v-if="product.original_price" class="price-original">
          {{ formatCurrency(product.original_price) }}
        </span>
        <span class="price-current">
          {{ formatCurrency(product.price) }}
        </span>
      </div>

      <!-- Actions -->
      <div class="product-actions">
        <button class="btn-primary" @click="handleBuy">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="9" cy="21" r="1"></circle>
            <circle cx="20" cy="21" r="1"></circle>
            <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
          </svg>
          Comprar
        </button>

        <button
          v-if="showViewButton"
          class="btn-icon"
          @click="handleView"
          title="Ver detalhes"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const props = defineProps({
  product: {
    type: Object,
    required: true,
  },
  showViewButton: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(['buy', 'view']);

const discount = computed(() => {
  if (props.product.original_price && props.product.price) {
    const discountPercent = Math.round(
      ((props.product.original_price - props.product.price) /
        props.product.original_price) *
        100
    );
    return discountPercent > 0 ? `-${discountPercent}%` : null;
  }
  return null;
});

const categoryColor = computed(() => {
  const colors = {
    Freios: '#dc2626',
    Motor: '#f59e0b',
    Suspensão: '#10b981',
    Elétrica: '#3b82f6',
    Filtros: '#8b5cf6',
    Escapamento: '#ec4899',
  };
  return colors[props.product.category_name] || '#6b7280';
});

const statusLabel = computed(() => {
  const labels = {
    sincronizado: 'ML Sincronizado',
    pendente: 'Pendente',
    erro: 'Erro',
  };
  return labels[props.product.ml_status] || 'Sem Status';
});

const formatCurrency = (value) => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
  }).format(value);
};

const handleBuy = () => {
  if (props.product.ml_link) {
    window.open(props.product.ml_link, '_blank');
  } else {
    emit('buy', props.product);
  }
};

const handleView = () => {
  router.push(`/produto/${props.product.id}`);
};
</script>

<style scoped>
.product-card {
  background-color: var(--color-bg-card);
  border-radius: var(--radius-lg);
  overflow: hidden;
  transition: all var(--transition-base);
  position: relative;
}

.product-card:hover {
  transform: translateY(-8px);
  box-shadow: var(--shadow-xl);
}

.discount-badge {
  position: absolute;
  top: var(--spacing-md);
  left: var(--spacing-md);
  background-color: var(--color-error);
  color: white;
  padding: var(--spacing-xs) var(--spacing-md);
  border-radius: var(--radius-full);
  font-size: var(--text-sm);
  font-weight: var(--font-bold);
  z-index: 10;
}

.product-image {
  width: 100%;
  aspect-ratio: 4/3;
  background-color: #e5e5e5;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.product-info {
  padding: var(--spacing-lg);
}

.category-badge,
.status-badge {
  display: inline-block;
  padding: var(--spacing-xs) var(--spacing-sm);
  font-size: var(--text-xs);
  font-weight: var(--font-semibold);
  border-radius: var(--radius-full);
  text-transform: uppercase;
  margin-right: var(--spacing-xs);
}

.status-badge.status-sincronizado {
  background-color: var(--color-success);
  color: white;
}

.status-badge.status-pendente {
  background-color: var(--color-warning);
  color: var(--color-bg-primary);
}

.status-badge.status-erro {
  background-color: var(--color-error);
  color: white;
}

.product-title {
  font-size: var(--text-lg);
  font-weight: var(--font-bold);
  color: var(--color-text-primary);
  margin: var(--spacing-sm) 0;
  text-transform: uppercase;
  line-height: 1.3;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  max-height: calc(1.3em * 2);
  line-clamp: 2;
}


.product-meta {
  font-size: var(--text-sm);
  color: var(--color-text-muted);
  margin-bottom: var(--spacing-md);
}

.product-price {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-lg);
}

.price-original {
  font-size: var(--text-base);
  color: var(--color-text-muted);
  text-decoration: line-through;
}

.price-current {
  font-size: var(--text-2xl);
  font-weight: var(--font-black);
  color: var(--color-primary);
}

.product-actions {
  display: flex;
  gap: var(--spacing-sm);
}

.product-actions .btn-primary {
  flex: 1;
}

.btn-icon {
  background-color: var(--color-bg-secondary);
  border: 1px solid var(--color-text-muted);
  color: var(--color-text-secondary);
  padding: var(--spacing-md);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-fast);
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-icon:hover {
  border-color: var(--color-primary);
  color: var(--color-primary);
  background-color: var(--color-bg-primary);
}
</style>
