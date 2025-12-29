<template>
  <div class="dashboard-layout">
    <DashboardSidebar />

    <main class="dashboard-main">
      <div class="dashboard-header">
        <div>
          <h1>Gerenciar Produtos</h1>
          <p>Todos os produtos cadastrados no sistema</p>
        </div>
        <router-link to="/dashboard/anunciador/novo" class="btn-primary">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="12" y1="5" x2="12" y2="19"></line>
            <line x1="5" y1="12" x2="19" y2="12"></line>
          </svg>
          Novo Produto
        </router-link>
      </div>

      <!-- Filters -->
      <div class="filters-bar">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Buscar por nome, marca ou SKU..."
          class="search-input"
          @input="handleSearch"
        />
        <select v-model="filterCategory" class="filter-select" @change="handleFilter">
          <option value="">Todas as Categorias</option>
          <option value="1">Freios</option>
          <option value="2">Motor</option>
          <option value="3">Suspensão</option>
          <option value="4">Elétrica</option>
          <option value="5">Filtros</option>
          <option value="6">Escapamento</option>
        </select>
        <select v-model="filterStatus" class="filter-select" @change="handleFilter">
          <option value="">Todos os Status</option>
          <option value="sincronizado">ML Sincronizado</option>
          <option value="pendente">Pendente</option>
          <option value="site">Apenas no Site</option>
        </select>
      </div>

      <!-- Products Table -->
      <div class="section-card">
        <div v-if="loading" class="loading-container">
          <div class="loading"></div>
          <p>Carregando produtos...</p>
        </div>

        <div v-else-if="products.length > 0" class="table-container">
          <table class="products-table">
            <thead>
              <tr>
                <th>Produto</th>
                <th>Categoria</th>
                <th>Marca</th>
                <th>SKU</th>
                <th>Preço</th>
                <th>Estoque</th>
                <th>Status</th>
                <th>Ações</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="product in products" :key="product.id">
                <td>
                  <div class="product-cell">
                    <div class="product-image">
                      <img :src="product.image || '/placeholder-product.png'" :alt="product.title" />
                    </div>
                    <div class="product-title">{{ product.title }}</div>
                  </div>
                </td>
                <td>
                  <span class="category-badge">{{ product.category }}</span>
                </td>
                <td>{{ product.brand }}</td>
                <td><code>{{ product.sku }}</code></td>
                <td class="price-cell">{{ formatCurrency(product.price) }}</td>
                <td>
                  <span
                    class="stock-badge"
                    :class="{ 'low-stock': product.stock < 10 }"
                  >
                    {{ product.stock }} un.
                  </span>
                </td>
                <td>
                  <span
                    class="status-badge"
                    :class="`status-${product.ml_status}`"
                  >
                    {{ getStatusLabel(product.ml_status) }}
                  </span>
                </td>
                <td>
                  <div class="action-buttons">
                    <button
                      v-if="product.ml_link"
                      class="btn-icon"
                      title="Ver no ML"
                      @click="openML(product.ml_link)"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
                        <polyline points="15 3 21 3 21 9"></polyline>
                        <line x1="10" y1="14" x2="21" y2="3"></line>
                      </svg>
                    </button>
                    <router-link
                      :to="`/dashboard/anunciador/editar/${product.id}`"
                      class="btn-icon"
                      title="Editar"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                        <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                      </svg>
                    </router-link>
                    <button
                      class="btn-icon btn-danger"
                      title="Excluir"
                      @click="handleDelete(product.id)"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <polyline points="3 6 5 6 21 6"></polyline>
                        <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                      </svg>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <p v-else class="no-data">Nenhum produto encontrado</p>
      </div>

      <!-- Pagination -->
      <div v-if="totalPages > 1" class="pagination">
        <button
          class="pagination-btn"
          :disabled="currentPage === 1"
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
          :disabled="currentPage === totalPages"
          @click="goToPage(currentPage + 1)"
        >
          Próxima
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="9 18 15 12 9 6"></polyline>
          </svg>
        </button>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import DashboardSidebar from '../components/layout/DashboardSidebar.vue';

const searchQuery = ref('');
const filterCategory = ref('');
const filterStatus = ref('');
const currentPage = ref(1);
const loading = ref(false);

const products = ref([
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
  {
    id: 4,
    title: 'Bobina de Ignição - Fiat Uno 2010-2017',
    brand: 'Bosch',
    sku: 'BI-UNO-2017',
    category: 'Elétrica',
    price: 159.90,
    stock: 15,
    ml_status: 'sincronizado',
    ml_link: 'https://mercadolivre.com/example',
    image: null,
  },
]);

const totalPages = computed(() => Math.ceil(products.value.length / 10));

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
    site: 'Apenas no Site',
  };
  return labels[status] || 'Sem Status';
};

const handleSearch = () => {
  console.log('Searching:', searchQuery.value);
};

const handleFilter = () => {
  console.log('Filtering:', filterCategory.value, filterStatus.value);
};

const openML = (link) => {
  if (link) {
    window.open(link, '_blank');
  }
};

const handleDelete = (id) => {
  if (confirm('Tem certeza que deseja excluir este produto?')) {
    products.value = products.value.filter(p => p.id !== id);
  }
};

const goToPage = (page) => {
  currentPage.value = page;
  window.scrollTo({ top: 0, behavior: 'smooth' });
};

onMounted(() => {
  // Fetch products
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

.filters-bar {
  display: flex;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-xl);
}

.search-input {
  flex: 1;
  padding: var(--spacing-md) var(--spacing-lg);
  background-color: var(--color-bg-card);
  border: 1px solid var(--color-text-muted);
  border-radius: var(--radius-md);
  color: var(--color-text-primary);
  font-size: var(--text-base);
}

.filter-select {
  min-width: 200px;
  padding: var(--spacing-md) var(--spacing-lg);
  background-color: var(--color-bg-card);
  border: 1px solid var(--color-text-muted);
  border-radius: var(--radius-md);
  color: var(--color-text-primary);
  font-size: var(--text-base);
}

.section-card {
  background-color: var(--color-bg-card);
  border-radius: var(--radius-lg);
  padding: var(--spacing-xl);
  margin-bottom: var(--spacing-xl);
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-3xl);
  gap: var(--spacing-lg);
}

.table-container {
  overflow-x: auto;
}

.products-table {
  width: 100%;
  border-collapse: collapse;
}

.products-table th {
  text-align: left;
  padding: var(--spacing-md);
  font-size: var(--text-sm);
  font-weight: var(--font-bold);
  color: var(--color-text-secondary);
  text-transform: uppercase;
  border-bottom: 2px solid var(--color-bg-secondary);
}

.products-table td {
  padding: var(--spacing-md);
  border-bottom: 1px solid var(--color-bg-secondary);
}

.products-table tbody tr {
  transition: background-color var(--transition-fast);
}

.products-table tbody tr:hover {
  background-color: var(--color-bg-secondary);
}

.product-cell {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.product-image {
  width: 50px;
  height: 50px;
  flex-shrink: 0;
  background-color: #e5e5e5;
  border-radius: var(--radius-md);
  overflow: hidden;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.product-title {
  font-weight: var(--font-semibold);
  max-width: 300px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.category-badge {
  display: inline-block;
  padding: var(--spacing-xs) var(--spacing-sm);
  background-color: var(--color-primary);
  color: var(--color-bg-primary);
  font-size: var(--text-xs);
  font-weight: var(--font-bold);
  border-radius: var(--radius-full);
  text-transform: uppercase;
}

.price-cell {
  font-weight: var(--font-bold);
  color: var(--color-primary);
}

.stock-badge {
  display: inline-block;
  padding: var(--spacing-xs) var(--spacing-sm);
  background-color: rgba(16, 185, 129, 0.2);
  color: var(--color-success);
  font-size: var(--text-sm);
  font-weight: var(--font-semibold);
  border-radius: var(--radius-md);
}

.stock-badge.low-stock {
  background-color: rgba(220, 38, 38, 0.2);
  color: var(--color-error);
}

.status-badge {
  display: inline-block;
  padding: var(--spacing-xs) var(--spacing-sm);
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

.status-badge.status-site {
  background-color: var(--color-info);
  color: white;
}

.action-buttons {
  display: flex;
  gap: var(--spacing-xs);
}

.btn-icon {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--color-bg-secondary);
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

.btn-icon.btn-danger:hover {
  border-color: var(--color-error);
  color: var(--color-error);
  background-color: rgba(220, 38, 38, 0.1);
}

.no-data {
  text-align: center;
  color: var(--color-text-secondary);
  padding: var(--spacing-3xl);
  margin: 0;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: var(--spacing-xl);
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

@media (max-width: 968px) {
  .dashboard-main {
    margin-left: 70px;
  }

  .dashboard-header {
    flex-direction: column;
    gap: var(--spacing-md);
    align-items: stretch;
  }

  .filters-bar {
    flex-direction: column;
  }

  .filter-select {
    width: 100%;
  }
}
</style>
