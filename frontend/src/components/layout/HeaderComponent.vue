<template>
  <header class="header">
    <div class="container header-content">
      <!-- Logo -->
      <router-link to="/" class="logo">
        <img src="C:\Users\arthu\Documents\ramon-autopecas\frontend\src\assets\logo.png" alt="Ramon Autopeças" />
      </router-link>

      <!-- Navigation -->
      <nav class="nav">
        <router-link
          to="/"
          class="nav-link"
          :class="{ active: $route.path === '/' }"
        >
          Início
        </router-link>
        <router-link
          to="/produtos"
          class="nav-link"
          :class="{ active: $route.path.includes('/produtos') }"
        >
          Produtos
        </router-link>
        <router-link
          to="/categorias"
          class="nav-link"
          :class="{ active: $route.path === '/categorias' }"
        >
          Categorias
        </router-link>
        <router-link
          to="/contato"
          class="nav-link"
          :class="{ active: $route.path === '/contato' }"
        >
          Contato
        </router-link>
      </nav>

      <!-- Search Bar -->
      <div class="search-bar">
        <input
          type="text"
          placeholder="Buscar peças..."
          v-model="searchQuery"
          @keyup.enter="handleSearch"
        />
        <button @click="handleSearch">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill="none"
            stroke="grey"
            stroke-width="2"
          >
            <circle cx="11" cy="11" r="8"></circle>
            <path d="m21 21-4.35-4.35"></path>
          </svg>
        </button>
      </div>

      <!-- Actions -->
      <div class="header-actions">
        <button class="icon-btn">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <circle cx="9" cy="21" r="1"></circle>
            <circle cx="20" cy="21" r="1"></circle>
            <path
              d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"
            ></path>
          </svg>
        </button>

        <router-link
          v-if="authStore.isAuthenticated"
          :to="
            authStore.isOwner
              ? '/dashboard/dono'
              : '/dashboard/anunciador'
          "
          class="btn-primary"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
            <circle cx="12" cy="7" r="4"></circle>
          </svg>
          Dashboard
        </router-link>

        <router-link v-else to="/login" class="btn-primary">
          Entrar
        </router-link>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../../stores/auth';

const router = useRouter();
const authStore = useAuthStore();
const searchQuery = ref('');

const handleSearch = () => {
  if (searchQuery.value.trim()) {
    router.push({
      name: 'products',
      query: { search: searchQuery.value },
    });
  }
};
</script>

<style scoped>
.header {
  position: sticky;
  top: 0;
  z-index: 100;
  background-color: var(--color-bg-primary);
  padding: 10px 0;
}

.header-content {
  display: flex;
  align-items: center;
  gap: var(--spacing-xl);
}

.logo {
  flex-shrink: 0;
}

.logo img {
  height: 45px;
  width: auto;
}

.nav {
  display: flex;
  gap: 15px;
}

.nav-link {
  color: var(--color-text-secondary);
  font-size: 0.9rem;
  font-weight: var(--font-medium);
  transition: color var(--transition-fast);
  position: relative;
}

.nav-link:hover,
.nav-link.active {
  color: var(--color-primary);
}

.nav-link.active::after {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 0;
  width: 100%;
  height: 2px;
}

.search-bar {
  flex: 1;
  max-width: 500px;
  position: relative;
  margin-left: 12vh;
}

.search-bar input {
  width: 100%;
  padding: var(--spacing-md) var(--spacing-lg);
  padding-right: 50px;
  background-color: var(--color-bg-secondary);
  border: 1px solid transparent;
  border-radius: 10px;
  color: var(--color-text-primary);
  font-size: 0.9rem;
  transition: all var(--transition-fast);
}

.search-bar input:focus {
  border-color: var(--color-primary);
  outline: none;
}

.search-bar button {
  position: absolute;
  right: 4px;
  top: 50%;
  transform: translateY(-50%);
  background-color: transparent;
  border: none;
  border-radius: var(--radius-full);
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color var(--transition-fast);
}

.search-bar button svg {
  color: var(--color-bg-primary);
}

.header-actions {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.icon-btn {
  background: transparent;
  border: none;
  color: var(--color-text-secondary);
  cursor: pointer;
  padding: var(--spacing-sm);
  border-radius: var(--radius-md);
  transition: all var(--transition-fast);
}

.icon-btn:hover {
  color: var(--color-primary);
  background-color: var(--color-bg-secondary);
}

@media (max-width: 1024px) {
  .nav {
    display: none;
  }
}

@media (max-width: 768px) {
  .search-bar {
    max-width: 200px;
  }
}
</style>
