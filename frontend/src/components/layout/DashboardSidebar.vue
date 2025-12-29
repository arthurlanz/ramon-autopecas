<template>
  <aside class="sidebar">
    <div class="sidebar-header">
      <img src="/logo.png" alt="Ramon Autopeças" class="sidebar-logo" />
      <span class="user-role">{{ roleLabel }}</span>
    </div>

    <nav class="sidebar-nav">
      <router-link
        :to="dashboardRoute"
        class="nav-item"
        :class="{ active: $route.path === dashboardRoute }"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="3" y="3" width="7" height="7"></rect>
          <rect x="14" y="3" width="7" height="7"></rect>
          <rect x="14" y="14" width="7" height="7"></rect>
          <rect x="3" y="14" width="7" height="7"></rect>
        </svg>
        <span>Visão Geral</span>
      </router-link>

      <router-link
        v-if="isAdvertiser"
        to="/dashboard/anunciador/meus-anuncios"
        class="nav-item"
        :class="{ active: $route.path.includes('meus-anuncios') }"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"></path>
          <line x1="7" y1="7" x2="7.01" y2="7"></line>
        </svg>
        <span>Meus Anúncios</span>
      </router-link>

      <router-link
        v-if="isAdvertiser"
        to="/dashboard/anunciador/novo"
        class="nav-item"
        :class="{ active: $route.path.includes('/novo') }"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="12" y1="5" x2="12" y2="19"></line>
          <line x1="5" y1="12" x2="19" y2="12"></line>
        </svg>
        <span>Novo Anúncio</span>
      </router-link>

      <router-link
        v-if="isAdvertiser"
        to="/dashboard/anunciador/sincronizar"
        class="nav-item"
        :class="{ active: $route.path.includes('sincronizar') }"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M21.5 2v6h-6M2.5 22v-6h6M2 11.5a10 10 0 0 1 18.8-4.3M22 12.5a10 10 0 0 1-18.8 4.2"/>
        </svg>
        <span>Sincronizar ML</span>
      </router-link>

      <router-link
        v-if="isOwner"
        to="/dashboard/dono/produtos"
        class="nav-item"
        :class="{ active: $route.path.includes('produtos') }"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"></path>
          <line x1="7" y1="7" x2="7.01" y2="7"></line>
        </svg>
        <span>Produtos</span>
      </router-link>

      <router-link
        v-if="isOwner"
        to="/dashboard/dono/vendas"
        class="nav-item"
        :class="{ active: $route.path.includes('vendas') }"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="9" cy="21" r="1"></circle>
          <circle cx="20" cy="21" r="1"></circle>
          <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
        </svg>
        <span>Vendas</span>
      </router-link>

      <router-link
        v-if="isOwner"
        to="/dashboard/dono/relatorios"
        class="nav-item"
        :class="{ active: $route.path.includes('relatorios') }"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="18" y1="20" x2="18" y2="10"></line>
          <line x1="12" y1="20" x2="12" y2="4"></line>
          <line x1="6" y1="20" x2="6" y2="14"></line>
        </svg>
        <span>Relatórios</span>
      </router-link>

      <router-link
        v-if="isOwner"
        to="/dashboard/dono/usuarios"
        class="nav-item"
        :class="{ active: $route.path.includes('usuarios') }"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
          <circle cx="9" cy="7" r="4"></circle>
          <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
          <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
        </svg>
        <span>Usuários</span>
      </router-link>

      <router-link
        to="/dashboard/configuracoes"
        class="nav-item"
        :class="{ active: $route.path.includes('configuracoes') }"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="3"></circle>
          <path d="M12 1v6m0 6v6m5.2-13.2l-4.2 4.2m0 6l4.2 4.2M1 12h6m6 0h6m-13.2-5.2l4.2 4.2m0 6l-4.2 4.2"></path>
        </svg>
        <span>Configurações</span>
      </router-link>
    </nav>

    <button class="sidebar-footer" @click="handleLogout">
      <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
        <polyline points="16 17 21 12 16 7"></polyline>
        <line x1="21" y1="12" x2="9" y2="12"></line>
      </svg>
      <span>Sair</span>
    </button>
  </aside>
</template>

<script setup>
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../../stores/auth';

const router = useRouter();
const authStore = useAuthStore();

const isOwner = computed(() => authStore.isOwner);
const isAdvertiser = computed(() => authStore.isAdvertiser);

const roleLabel = computed(() => {
  return isOwner.value ? 'Proprietário' : 'Anunciador';
});

const dashboardRoute = computed(() => {
  return isOwner.value ? '/dashboard/dono' : '/dashboard/anunciador';
});

const handleLogout = () => {
  authStore.logout();
  router.push('/login');
};
</script>

<style scoped>
.sidebar {
  width: var(--sidebar-width);
  height: 100vh;
  background-color: var(--color-bg-secondary);
  border-right: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  flex-direction: column;
  position: fixed;
  left: 0;
  top: 0;
  z-index: 50;
}

.sidebar-header {
  padding: var(--spacing-xl);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.sidebar-logo {
  height: 40px;
  width: auto;
  margin-bottom: var(--spacing-sm);
}

.user-role {
  display: inline-block;
  padding: var(--spacing-xs) var(--spacing-md);
  background-color: var(--color-primary);
  color: var(--color-bg-primary);
  font-size: var(--text-xs);
  font-weight: var(--font-bold);
  border-radius: var(--radius-full);
  text-transform: uppercase;
}

.sidebar-nav {
  flex: 1;
  padding: var(--spacing-lg) 0;
  overflow-y: auto;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-md) var(--spacing-xl);
  color: var(--color-text-secondary);
  font-size: var(--text-base);
  font-weight: var(--font-medium);
  transition: all var(--transition-fast);
  border-left: 3px solid transparent;
}

.nav-item:hover {
  background-color: var(--color-bg-primary);
  color: var(--color-primary);
}

.nav-item.active {
  background-color: var(--color-card-products);
  color: var(--color-primary);
  border-left-color: var(--color-primary);
}

.nav-item svg {
  flex-shrink: 0;
}

.sidebar-footer {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-lg) var(--spacing-xl);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  background: transparent;
  border-left: none;
  border-right: none;
  border-bottom: none;
  color: var(--color-text-secondary);
  font-size: var(--text-base);
  font-weight: var(--font-medium);
  cursor: pointer;
  transition: all var(--transition-fast);
  width: 100%;
  text-align: left;
}

.sidebar-footer:hover {
  background-color: var(--color-error);
  color: white;
}

@media (max-width: 768px) {
  .sidebar {
    width: 70px;
  }

  .sidebar-header,
  .nav-item span,
  .sidebar-footer span,
  .user-role {
    display: none;
  }

  .nav-item {
    justify-content: center;
    padding: var(--spacing-md);
  }

  .sidebar-footer {
    justify-content: center;
  }
}
</style>
