<template>
  <div class="home">
    <HeaderComponent />
    <HeroSection />

    <!-- Categories -->
    <section class="categories-section">
      <div class="container">
        <div class="section-header">
          <h2>Categorias</h2>
          <router-link to="/categorias" class="view-all">
            Ver Todas
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="5" y1="12" x2="19" y2="12"></line>
              <polyline points="12 5 19 12 12 19"></polyline>
            </svg>
          </router-link>
        </div>

        <div class="grid grid-6">
          <CategoryCard
            v-for="category in categories"
            :key="category.id"
            :category="category"
          />
        </div>
      </div>
    </section>

    <!-- Featured Products -->
    <section class="featured-products">
      <div class="container">
        <div class="section-header">
          <h2>Produtos em Destaque</h2>
          <p>Confira nossas melhores ofertas sincronizadas com o Mercado Livre</p>
        </div>

        <ProductGrid
          :products="featuredProducts"
          :loading="loading"
        />

        <div class="text-center">
          <router-link to="/produtos" class="btn-primary">
            Ver Todos os Produtos
          </router-link>
        </div>
      </div>
    </section>

    <!-- CTA Mercado Livre -->
    <section class="cta-ml">
      <div class="container">
        <h2>Também Vendemos no Mercado Livre</h2>
        <p>
          Confira nossa loja oficial no Mercado Livre e aproveite as mesmas ofertas com a
          segurança da maior plataforma de e-commerce da América Latina.
        </p>
        <a :href="mlStoreUrl" target="_blank" class="btn-primary">
          Visitar Loja no Mercado Livre
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="5" y1="12" x2="19" y2="12"></line>
            <polyline points="12 5 19 12 12 19"></polyline>
          </svg>
        </a>
      </div>
    </section>

    <FooterComponent />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useProductsStore } from '../stores/products';
import HeaderComponent from '../components/layout/HeaderComponent.vue';
import HeroSection from '../components/home/HeroSection.vue';
import FooterComponent from '../components/layout/FooterComponent.vue';
import ProductGrid from '../components/products/ProductGrid.vue';
import CategoryCard from '../components/products/CategoryCard.vue';

const productsStore = useProductsStore();
const mlStoreUrl = import.meta.env.VITE_ML_STORE_URL || 'https://www.mercadolivre.com.br';

const featuredProducts = ref([]);
const categories = ref([]);
const loading = ref(false);

onMounted(async () => {
  loading.value = true;
  try {
    await Promise.all([
      productsStore.fetchFeaturedProducts(),
      productsStore.fetchCategories(),
    ]);

    featuredProducts.value = productsStore.featuredProducts;
    categories.value = productsStore.categories.slice(0, 6);
  } catch (error) {
    console.error('Error loading home data:', error);
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.home {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* Categories Section */
.categories-section {
  padding: var(--spacing-3xl) 0;
  background-color: var(--color-bg-secondary);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-2xl);
}

.section-header h2 {
  margin: 0;
}

.view-all {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  font-weight: var(--font-semibold);
}

.grid-6 {
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
}

/* Featured Products */
.featured-products {
  padding: var(--spacing-3xl) 0;
  background-color: var(--color-bg-secondary);
}

.section-header p {
  color: var(--color-text-secondary);
  font-size: var(--text-base);
}

/* CTA ML */
.cta-ml {
  padding: var(--spacing-3xl) 0;
  background: linear-gradient(135deg, rgba(253, 184, 19, 0.1) 0%, rgba(16, 185, 129, 0.1) 100%);
  text-align: center;
}

.cta-ml h2 {
  margin-bottom: var(--spacing-lg);
}

.cta-ml p {
  max-width: 700px;
  margin: 0 auto var(--spacing-xl);
  color: var(--color-text-secondary);
}

@media (max-width: 768px) {
  .section-header {
    flex-direction: column;
    gap: var(--spacing-md);
    text-align: center;
  }
}
</style>
