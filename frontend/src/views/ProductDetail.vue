<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useProductsStore } from '../stores/products';
import HeaderComponent from '../components/layout/HeaderComponent.vue';
import FooterComponent from '../components/layout/FooterComponent.vue';

const route = useRoute();
const productsStore = useProductsStore();

const product = ref(null);
const loading = ref(true);
const selectedImage = ref(0);

const images = computed(() => {
  if (!product.value) return [];
  return product.value.images || [];
});

const formatCurrency = (value) => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
  }).format(value);
};

onMounted(async () => {
  try {
    const slug = route.params.slug;
    product.value = await productsStore.fetchProduct(slug);

    if (images.value.length > 0) {
      selectedImage.value = 0;
    }
  } catch (error) {
    console.error('Error loading product:', error);
  } finally {
    loading.value = false;
  }
});
</script>

<template>
  <div class="product-detail-page">
    <HeaderComponent />

    <div v-if="loading" class="loading-container">
      <div class="loading"></div>
      <p>Carregando produto...</p>
    </div>

    <div v-else-if="product" class="container page-content">
      <div class="product-detail">
        <!-- Images -->
        <div class="product-images">
          <div class="main-image">
            <img
              :src="images[selectedImage]?.image_url || product.primary_image || '/placeholder-product.png'"
              :alt="product.title"
            />
          </div>
          <div v-if="images.length > 1" class="image-thumbnails">
            <button
              v-for="(image, index) in images"
              :key="index"
              class="thumbnail"
              :class="{ active: selectedImage === index }"
              @click="selectedImage = index"
            >
              <img :src="image.image_url" :alt="`${product.title} - ${index + 1}`" />
            </button>
          </div>
        </div>

        <!-- Info -->
        <div class="product-info">
          <div class="breadcrumb">
            <router-link to="/">Home</router-link>
            <span>/</span>
            <router-link to="/produtos">Produtos</router-link>
            <span>/</span>
            <span>{{ product.category_name }}</span>
          </div>

          <h1>{{ product.title }}</h1>

          <div class="product-meta">
            <span class="brand">{{ product.brand }}</span>
            <span class="sku">SKU: {{ product.sku }}</span>
            <span
              class="stock-badge"
              :class="{ 'low-stock': product.is_low_stock, 'out-stock': product.stock_quantity === 0 }"
            >
              {{ product.stock_quantity > 0 ? `${product.stock_quantity} em estoque` : 'Sem estoque' }}
            </span>
          </div>

          <div class="price-section">
            <div class="price">{{ formatCurrency(product.price) }}</div>
            <p class="installments">Em até 12x sem juros</p>
          </div>

          <div v-if="product.compatible_vehicles" class="compatibility">
            <h3>Compatibilidade</h3>
            <p>{{ product.compatible_vehicles }}</p>
            <p v-if="product.year_from || product.year_to" class="years">
              Ano: {{ product.year_from }} - {{ product.year_to }}
            </p>
          </div>

          <div class="actions">
            <button
              class="btn-primary"
              :disabled="product.stock_quantity === 0"
              @click="addToCart"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="9" cy="21" r="1"></circle>
                <circle cx="20" cy="21" r="1"></circle>
                <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
              </svg>
              {{ product.stock_quantity === 0 ? 'Indisponível' : 'Comprar' }}
            </button>

            <a
              v-if="product.ml_permalink"
              :href="product.ml_permalink"
              target="_blank"
              class="btn-secondary"
            >
              Ver no Mercado Livre
            </a>
          </div>

          <div class="product-description">
            <h2>Descrição</h2>
            <p>{{ product.description }}</p>
          </div>

          <div class="product-specs">
            <h2>Especificações</h2>
            <table>
              <tr>
                <td>Marca</td>
                <td>{{ product.brand }}</td>
              </tr>
              <tr v-if="product.model">
                <td>Modelo</td>
                <td>{{ product.model }}</td>
              </tr>
              <tr>
                <td>SKU</td>
                <td>{{ product.sku }}</td>
              </tr>
              <tr v-if="product.barcode">
                <td>Código de Barras</td>
                <td>{{ product.barcode }}</td>
              </tr>
              <tr>
                <td>Condição</td>
                <td>{{ product.condition === 'new' ? 'Novo' : 'Usado' }}</td>
              </tr>
              <tr v-if="product.weight">
                <td>Peso</td>
                <td>{{ product.weight }} kg</td>
              </tr>
            </table>
          </div>
        </div>
      </div>
    </div>

    <FooterComponent />
  </div>
</template>
<style scoped>
.product-detail-page {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.loading-container,
.error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
  gap: var(--spacing-lg);
}

.error-container svg {
  color: var(--color-error);
}

/* Breadcrumb */
.breadcrumb {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  margin: var(--spacing-xl) 0;
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
}

.breadcrumb a {
  color: var(--color-text-secondary);
}

.breadcrumb a:hover {
  color: var(--color-primary);
}

/* Product Content */
.product-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-3xl);
  margin-bottom: var(--spacing-3xl);
}

/* Images */
.product-images {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.main-image {
  width: 100%;
  aspect-ratio: 1;
  background-color: #e5e5e5;
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.main-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-thumbs {
  display: flex;
  gap: var(--spacing-md);
  overflow-x: auto;
}

.image-thumbs img {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: var(--radius-md);
  cursor: pointer;
  opacity: 0.6;
  transition: all var(--transition-fast);
  border: 2px solid transparent;
}

.image-thumbs img:hover,
.image-thumbs img.active {
  opacity: 1;
  border-color: var(--color-primary);
}

/* Product Info */
.product-info {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.category-badge {
  display: inline-block;
  width: fit-content;
  padding: var(--spacing-xs) var(--spacing-md);
  background-color: var(--color-primary);
  color: var(--color-bg-primary);
  font-size: var(--text-xs);
  font-weight: var(--font-bold);
  border-radius: var(--radius-full);
  text-transform: uppercase;
}

.product-info h1 {
  font-size: var(--text-3xl);
  margin: 0;
}

.product-meta {
  display: flex;
  gap: var(--spacing-xl);
  color: var(--color-text-secondary);
}

.product-price {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.price-original {
  font-size: var(--text-xl);
  color: var(--color-text-muted);
  text-decoration: line-through;
}

.price-current {
  font-size: var(--text-4xl);
  font-weight: var(--font-black);
  color: var(--color-primary);
}

.stock-info {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-md);
  background-color: rgba(16, 185, 129, 0.1);
  border-radius: var(--radius-md);
  color: var(--color-success);
  font-weight: var(--font-semibold);
}

.stock-info.out-of-stock {
  background-color: rgba(220, 38, 38, 0.1);
  color: var(--color-error);
}

.product-description h3 {
  font-size: var(--text-xl);
  margin-bottom: var(--spacing-sm);
}

.product-description p {
  color: var(--color-text-secondary);
  line-height: 1.8;
}

.btn-large {
  padding: var(--spacing-lg) var(--spacing-2xl);
  font-size: var(--text-lg);
  width: 100%;
}

.sync-status {
  padding-top: var(--spacing-md);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.status-badge {
  display: inline-block;
  padding: var(--spacing-xs) var(--spacing-md);
  font-size: var(--text-xs);
  font-weight: var(--font-semibold);
  border-radius: var(--radius-full);
  text-transform: uppercase;
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

@media (max-width: 768px) {
  .product-content {
    grid-template-columns: 1fr;
  }
}
</style>
