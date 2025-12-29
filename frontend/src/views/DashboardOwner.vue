<template>
  <div class="dashboard-layout">
    <DashboardSidebar />

    <main class="dashboard-main">
      <div class="dashboard-header">
        <div>
          <h1>Painel do Proprietário</h1>
          <p>Visão geral do seu negócio</p>
        </div>
      </div>

      <!-- Stats Cards -->
      <div class="stats-grid">
        <StatsCard
          label="Total de Produtos"
          :value="stats.totalProducts"
          bg-color="var(--color-card-products)"
          icon-bg-color="var(--color-primary)"
        >
          <template #icon>
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"></path>
              <line x1="7" y1="7" x2="7.01" y2="7"></line>
            </svg>
          </template>
        </StatsCard>

        <StatsCard
          label="Vendas do Mês"
          :value="stats.monthlySales"
          type="currency"
          change="+12,5% vs. mês anterior"
          bg-color="var(--color-card-sales)"
          icon-bg-color="var(--color-success)"
        >
          <template #icon>
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="12" y1="1" x2="12" y2="23"></line>
              <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
            </svg>
          </template>
        </StatsCard>

        <StatsCard
          label="Pedidos Pendentes"
          :value="stats.pendingOrders"
          bg-color="var(--color-card-pending)"
          icon-bg-color="var(--color-warning)"
        >
          <template #icon>
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="9" cy="21" r="1"></circle>
              <circle cx="20" cy="21" r="1"></circle>
              <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
            </svg>
          </template>
        </StatsCard>

        <StatsCard
          label="Estoque Baixo"
          :value="stats.lowStock"
          bg-color="var(--color-card-stock)"
          icon-bg-color="var(--color-error)"
        >
          <template #icon>
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"></path>
              <line x1="12" y1="9" x2="12" y2="13"></line>
              <line x1="12" y1="17" x2="12.01" y2="17"></line>
            </svg>
          </template>
        </StatsCard>
      </div>

      <!-- Charts -->
      <div class="charts-grid">
        <div class="chart-card">
          <div class="chart-header">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="12" y1="20" x2="12" y2="10"></line>
              <line x1="18" y1="20" x2="18" y2="4"></line>
              <line x1="6" y1="20" x2="6" y2="16"></line>
            </svg>
            <h3>Vendas dos Últimos Dias</h3>
          </div>
          <BarChart :data="salesChartData" />
        </div>

        <div class="chart-card">
          <div class="chart-header">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"></path>
              <path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"></path>
            </svg>
            <h3>Vendas por Plataforma</h3>
          </div>
          <div class="donut-chart">
            <svg width="200" height="200" viewBox="0 0 200 200">
              <circle cx="100" cy="100" r="80" fill="none" stroke="var(--color-primary)" stroke-width="30" stroke-dasharray="440 503" transform="rotate(-90 100 100)"></circle>
              <circle cx="100" cy="100" r="80" fill="none" stroke="var(--color-success)" stroke-width="30" stroke-dasharray="63 503" stroke-dashoffset="-440" transform="rotate(-90 100 100)"></circle>
            </svg>
            <div class="donut-legend">
              <div class="legend-item">
                <span class="legend-color" style="background: var(--color-primary)"></span>
                <span>Site</span>
              </div>
              <div class="legend-item">
                <span class="legend-color" style="background: var(--color-success)"></span>
                <span>Mercado Livre</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Low Stock Alert -->
      <div class="alert-card">
        <div class="alert-header">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"></path>
            <line x1="12" y1="9" x2="12" y2="13"></line>
            <line x1="12" y1="17" x2="12.01" y2="17"></line>
          </svg>
          <h3>Produtos com Estoque Baixo</h3>
        </div>

        <div v-if="lowStockProducts.length > 0" class="low-stock-list">
          <div
            v-for="product in lowStockProducts"
            :key="product.id"
            class="low-stock-item"
          >
            <div class="product-info">
              <h4>{{ product.title }}</h4>
              <p>{{ product.brand }} | SKU: {{ product.sku }}</p>
            </div>
            <span class="stock-badge">{{ product.stock }} em estoque</span>
          </div>
        </div>
        <p v-else class="no-data">Nenhum produto com estoque baixo</p>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useDashboardStore } from '../stores/dashboard';
import DashboardSidebar from '../components/layout/DashboardSidebar.vue';
import StatsCard from '../components/dashboard/StatsCard.vue';
import BarChart from '../components/dashboard/BarChart.vue';

const dashboardStore = useDashboardStore();

const stats = ref({
  totalProducts: 0,
  monthlySales: 0,
  pendingOrders: 0,
  lowStock: 0,
});

const salesChartData = ref({
  labels: [],
  datasets: [{
    label: 'Vendas (R$)',
    data: [],
    backgroundColor: '#FDB813',
    borderRadius: 8,
  }],
});

const lowStockProducts = ref([]);

onMounted(async () => {
  await dashboardStore.fetchAll();

  if (dashboardStore.overview) {
    stats.value = {
      totalProducts: dashboardStore.overview.products.total,
      monthlySales: dashboardStore.overview.orders.month_revenue,
      pendingOrders: dashboardStore.overview.orders.pending,
      lowStock: dashboardStore.overview.products.low_stock,
    };
  }

  if (dashboardStore.salesChart.length > 0) {
    salesChartData.value = {
      labels: dashboardStore.salesChart.slice(-7).map(item => {
        const date = new Date(item.date);
        return `${date.getDate()}/${date.getMonth() + 1}`;
      }),
      datasets: [{
        label: 'Vendas (R$)',
        data: dashboardStore.salesChart.slice(-7).map(item => item.revenue),
        backgroundColor: '#FDB813',
        borderRadius: 8,
      }],
    };
  }
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

.charts-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-2xl);
}

.chart-card {
  background-color: var(--color-bg-card);
  border-radius: var(--radius-lg);
  padding: var(--spacing-xl);
}

.chart-header {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-xl);
}

.chart-header svg {
  color: var(--color-primary);
}

.chart-header h3 {
  font-size: var(--text-xl);
  font-weight: var(--font-black);
  text-transform: uppercase;
}

.donut-chart {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-xl);
}

.donut-legend {
  display: flex;
  gap: var(--spacing-lg);
}

.legend-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.legend-color {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.alert-card {
  background-color: rgba(220, 38, 38, 0.1);
  border: 1px solid var(--color-error);
  border-radius: var(--radius-lg);
  padding: var(--spacing-xl);
}

.alert-header {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-lg);
}

.alert-header svg {
  color: var(--color-error);
}

.alert-header h3 {
  font-size: var(--text-xl);
  font-weight: var(--font-black);
  text-transform: uppercase;
  color: var(--color-error);
}

.low-stock-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.low-stock-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-md);
  background-color: var(--color-bg-card);
  border-radius: var(--radius-md);
}

.product-info h4 {
  font-size: var(--text-base);
  margin-bottom: var(--spacing-xs);
}

.product-info p {
  font-size: var(--text-sm);
  color: var(--color-text-muted);
  margin: 0;
}

.stock-badge {
  padding: var(--spacing-xs) var(--spacing-md);
  background-color: var(--color-error);
  color: white;
  font-size: var(--text-sm);
  font-weight: var(--font-bold);
  border-radius: var(--radius-full);
}

.no-data {
  text-align: center;
  color: var(--color-text-secondary);
  padding: var(--spacing-xl);
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

  .charts-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>
