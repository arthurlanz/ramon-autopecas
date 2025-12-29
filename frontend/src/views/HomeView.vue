<template>
  <div class="home">
    <HeaderComponent />
    <section class="hero">
      <div class="container">
        <h1>
          Peças de <span class="highlight">Qualidade</span><br />
          Para Seu Veículo
        </h1>
        <p class="hero-description">
          Encontre as melhores peças automotivas com preços imbatíveis. Qualidade
          garantida e entrega rápida para todo o Brasil.
        </p>
        <div class="hero-actions">
          <router-link to="/produtos" class="btn-primary">
            Ver Produtos
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="5" y1="12" x2="19" y2="12"></line>
              <polyline points="12 5 19 12 12 19"></polyline>
            </svg>
          </router-link>
          <a :href="mlStoreUrl" target="_blank" class="btn-primary">
            Nossa Loja no ML
          </a>
        </div>
      </div>
    </section>

    <!-- Features -->
    <section class="features">
      <div class="container">
        <div class="feature-card">
          <div class="feature-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="1" y="3" width="15" height="13"></rect>
              <polygon points="16 8 20 8 23 11 23 16 16 16 16 8"></polygon>
              <circle cx="5.5" cy="18.5" r="2.5"></circle>
              <circle cx="18.5" cy="18.5" r="2.5"></circle>
            </svg>
          </div>
          <h3>Entrega Rápida</h3>
          <p>Enviamos para todo o Brasil</p>
        </div>

        <div class="feature-card">
          <div class="feature-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
            </svg>
          </div>
          <h3>Garantia</h3>
          <p>Todos os produtos com garantia</p>
        </div>

        <div class="feature-card">
          <div class="feature-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="1" y="4" width="22" height="16" rx="2" ry="2"></rect>
              <line x1="1" y1="10" x2="23" y2="10"></line>
            </svg>
          </div>
          <h3>Parcelamento</h3>
          <p>Em até 12x sem juros</p>
        </div>
      </div>
    </section>

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

/* Hero Section */
.hero {
  padding: var(--spacing-3xl) 0;
  text-align: center;
  background: linear-gradient(180deg, var(--color-bg-secondary) 0%, var(--color-bg-primary) 100%);
}

.hero h1 {
  font-size: clamp(2.5rem, 5vw, 4rem);
  font-weight: var(--font-black);
  line-height: 1.1;
  margin-bottom: var(--spacing-lg);
}

.hero .highlight {
  color: var(--color-primary);
}

.hero-description {
  font-size: var(--text-lg);
  color: var(--color-text-secondary);
  max-width: 600px;
  margin: 0 auto var(--spacing-2xl);
}

.hero-actions {
  display: flex;
  gap: var(--spacing-md);
  justify-content: center;
  flex-wrap: wrap;
}

/* Features */
.features {
  padding: var(--spacing-3xl) 0;
  background-color: var(--color-bg-secondary);
}

.features .container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--spacing-xl);
}

.feature-card {
  background-color: var(--color-bg-card);
  padding: var(--spacing-2xl);
  border-radius: var(--radius-lg);
  text-align: center;
  transition: all var(--transition-base);
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-xl);
}

.feature-icon {
  width: 70px;
  height: 70px;
  margin: 0 auto var(--spacing-lg);
  background-color: rgba(253, 184, 19, 0.2);
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
}

.feature-icon svg {
  color: var(--color-primary);
}

.feature-card h3 {
  font-size: var(--text-xl);
  font-weight: var(--font-bold);
  margin-bottom: var(--spacing-sm);
}

.feature-card p {
  color: var(--color-text-secondary);
  margin: 0;
}

/* Categories Section */
.categories-section {
  padding: var(--spacing-3xl) 0;
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
