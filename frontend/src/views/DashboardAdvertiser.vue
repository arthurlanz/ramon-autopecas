<template>
  <div class="dashboard-layout">
    <DashboardSidebar />

    <main class="dashboard-main">
      <div class="dashboard-header">
        <div>
          <h1>Painel do Anunciador</h1>
          <p>Gerencie seus anúncios</p>
        </div>
        <router-link to="/dashboard/anunciador/novo" class="btn-primary">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="12" y1="5" x2="12" y2="19"></line>
            <line x1="5" y1="12" x2="19" y2="12"></line>
          </svg>
          Novo Anúncio
        </router-link>
      </div>

      <!-- Stats Cards -->
      <div class="stats-grid">
        <StatsCard
          label="Total de Anúncios"
          :value="stats.totalAds"
          bg-color="var(--color-card-products)"
          icon-bg-color="var(--color-primary)"
        >
          <template #icon>
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"></path>
            </svg>
          </template>
        </StatsCard>

        <StatsCard
          label="Sincronizados com ML"
          :value="stats.syncedAds"
          bg-color="var(--color-card-sales)"
          icon-bg-color="var(--color-success)"
        >
          <template #icon>
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="20 6 9 17 4 12"></polyline>
            </svg>
          </template>
        </StatsCard>

        <StatsCard
          label="Pendentes"
          :value="stats.pendingAds"
          bg-color="var(--color-card-pending)"
          icon-bg-color="var(--color-warning)"
        >
          <template #icon>
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"></circle>
              <polyline points="12 6 12 12 16 14"></polyline>
            </svg>
          </template>
        </StatsCard>

        <StatsCard
          label="Apenas no Site"
          :value="stats.siteOnlyAds"
          bg-color="rgba(59, 130, 246, 0.1)"
          icon-bg-color="var(--color-info)"
        >
          <template #icon>
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="2" y1="12" x2="22" y2="12"></line>
              <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>
            </svg>
          </template>
        </StatsCard>
      </div>

      <!-- Recent Ads -->
      <div class="section-card">
        <div class="section-header">
          <h2>Meus Anúncios Recentes</h2>
          <button class="btn-sync" @click="syncAllWithML">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21.5 2v6h-6M2.5 22v-6h6M2 11.5a10 10 0 0 1 18.8-4.3M22 12.5a10 10 0 0 1-18.8 4.2"/>
            </svg>
            Sincronizar com ML
          </button>
        </div>

        <div v-if="recentAds.length > 0" class="ads-list">
          <div
            v-for="ad in recentAds"
            :key="ad.id"
            class="ad-item"
          >
            <div class="ad-image">
              <img :src="ad.image || '/placeholder-product.png'" :alt="ad.title" />
            </div>
            <div class="ad-info">
              <div>
                <span class="category-badge">{{ ad.category }}</span>
                <span
                  class="status-badge"
                  :class="`status-${ad.ml_status}`"
                >
                  {{ getStatusLabel(ad.ml_status) }}
                </span>
              </div>
              <h3>{{ ad.title }}</h3>
              <p>{{ ad.brand }} | SKU: {{ ad.sku }}</p>
              <div class="ad-meta">
                <span class="price">{{ formatCurrency(ad.price) }}</span>
                <span class="stock">{{ ad.stock }} un.</span>
              </div>
            </div>
            <div class="ad-actions">
              <button class="btn-icon" title="Ver no ML" @click="openML(ad.ml_link)">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
                  <polyline points="15 3 21 3 21 9"></polyline>
                  <line x1="10" y1="14" x2="21" y2="3"></line>
                </svg>
              </button>
              <router-link :to="`/dashboard/anunciador/editar/${ad.id}`" class="btn-icon" title="Editar">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                  <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                </svg>
              </router-link>
            </div>
          </div>
        </div>
        <p v-else class="no-data">Nenhum anúncio criado ainda</p>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import DashboardSidebar from '../components/layout/DashboardSidebar.vue';
import StatsCard from '../components/dashboard/StatsCard.vue';

const stats = ref({
  totalAds: 6,
  syncedAds: 4,
  pendingAds: 1,
  siteOnlyAds: 1,
});

const recentAds = ref([
  {
    id: 1,
    title: 'Pastilha de Freio Dianteira - Honda Civic 2016-2021',
    brand: 'Fras-le',
    sku: 'PFD-HC-2021',
    category: 'Freios',
    price: 189.90,
    stock: 25,
    ml_status: 'sincronizado',
    ml_link: 'https://mercadolivre.com/example',
    image: null,
  },
  {
    id: 2,
    title: 'Filtro de Óleo - Toyota Corolla 2018-2023',
    brand: 'Tecfil',
    sku: 'FO-TC-2023',
    category: 'Filtros',
    price: 45.90,
    stock: 50,
    ml_status: 'sincronizado',
    ml_link: 'https://mercadolivre.com/example',
    image: null,
  },
  {
    id: 3,
    title: 'Amortecedor Dianteiro - VW Gol G5/G6',
    brand: 'Cofap',
    sku: 'AD-GOL-G6',
    category: 'Suspensão',
    price: 320.00,
    stock: 8,
    ml_status: 'pendente',
    ml_link: null,
    image: null,
  },
]);

const formatCurrency = (value) => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
  }).format(value);
};

const getStatusLabel = (status) => {
  const labels = {
    sincronizado: 'ML Sincronizado',
    pendente: 'Pendente',
    erro: 'Erro',
  };
  return labels[status] || 'Sem Status';
};

const syncAllWithML = () => {
  alert('Sincronizando todos os produtos com o Mercado Livre...');
};

const openML = (link) => {
  if (link) {
    window.open(link, '_blank');
  }
};

onMounted(() => {
  // Fetch advertiser data
});
</script>

<style scoped>
.dashboard-layout {
  display: flex;
  min-height: 100vh;
  background-color: var(--color-bg-primary);
}

.dashboard-main {
  margin-left: var(--sidebar-width);
  flex: 1;
  padding: var(--spacing-2xl);
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-2xl);
}

.dashboard-header h1 {
  font-size: var(--text-3xl);
  margin-bottom: var(--spacing-xs);
}

.dashboard-header p {
  color: var(--color-text-secondary);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-2xl);
}

.section-card {
  background-color: var(--color-bg-card);
  border-radius: var(--radius-lg);
  padding: var(--spacing-xl);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-xl);
}

.section-header h2 {
  font-size: var(--text-2xl);
  font-weight: var(--font-black);
  text-transform: uppercase;
  margin: 0;
}

.btn-sync {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-sm) var(--spacing-lg);
  background-color: var(--color-bg-secondary);
  border: 1px solid var(--color-primary);
  border-radius: var(--radius-md);
  color: var(--color-primary);
  font-weight: var(--font-semibold);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.btn-sync:hover {
  background-color: var(--color-primary);
  color: var(--color-bg-primary);
}

.ads-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.ad-item {
  display: flex;
  gap: var(--spacing-lg);
  padding: var(--spacing-lg);
  background-color: var(--color-bg-secondary);
  border-radius: var(--radius-md);
  transition: all var(--transition-fast);
}

.ad-item:hover {
  background-color: var(--color-bg-card-hover);
}

.ad-image {
  width: 100px;
  height: 100px;
  flex-shrink: 0;
  background-color: #e5e5e5;
  border-radius: var(--radius-md);
  overflow: hidden;
}

.ad-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.ad-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
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

.category-badge {
  background-color: var(--color-primary);
  color: var(--color-bg-primary);
}

.status-badge.status-sincronizado {
  background-color: var(--color-success);
  color: white;
}

.status-badge.status-pendente {
  background-color: var(--color-warning);
  color: var(--color-bg-primary);
}

.ad-info h3 {
  font-size: var(--text-lg);
  font-weight: var(--font-bold);
  margin: 0;
}

.ad-info p {
  color: var(--color-text-muted);
  font-size: var(--text-sm);
  margin: 0;
}

.ad-meta {
  display: flex;
  gap: var(--spacing-lg);
  align-items: center;
}

.price {
  font-size: var(--text-xl);
  font-weight: var(--font-black);
  color: var(--color-primary);
}

.stock {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
}

.ad-actions {
  display: flex;
  gap: var(--spacing-sm);
  align-items: center;
}

.btn-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--color-bg-primary);
  border: 1px solid var(--color-text-muted);
  border-radius: var(--radius-md);
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.btn-icon:hover {
  border-color: var(--color-primary);
  color: var(--color-primary);
}

.no-data {
  text-align: center;
  color: var(--color-text-secondary);
  padding: var(--spacing-3xl);
  margin: 0;
}

@media (max-width: 1400px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 968px) {
  .dashboard-main {
    margin-left: 70px;
  }

  .dashboard-header {
    flex-direction: column;
    gap: var(--spacing-md);
    align-items: stretch;
  }
}

@media (max-width: 640px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }

  .ad-item {
    flex-direction: column;
  }
}
</style>
