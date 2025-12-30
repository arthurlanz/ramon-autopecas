<template>
  <header class="header">
    <div class="container header-content">
      <!-- Logo -->
      <router-link to="/" class="logo">
        <img src="@/assets/logo.png" alt="Ramon Autopeças" />
      </router-link>

      <!-- Desktop Navigation -->
      <nav class="nav">
        <router-link
          v-for="link in navLinks"
          :key="link.href"
          :to="link.href"
          class="nav-link"
          :class="{ active: isActive(link.href) }"
        >
          {{ link.label }}
        </router-link>
      </nav>

      <!-- Search Bar -->
      <div class="search-bar">
        <svg
          class="search-icon"
          xmlns="http://www.w3.org/2000/svg"
          width="20"
          height="20"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
        >
          <circle cx="11" cy="11" r="8"></circle>
          <path d="m21 21-4.35-4.35"></path>
        </svg>
        <input
          type="search"
          placeholder="Buscar peças..."
          v-model="searchQuery"
          @keyup.enter="handleSearch"
        />
      </div>

      <!-- Actions -->
      <div class="header-actions">
        <button class="icon-btn cart-btn">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <circle cx="9" cy="21" r="1"></circle>
            <circle cx="20" cy="21" r="1"></circle>
            <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
          </svg>
        </button>

        <router-link to="/login" class="btn-entrar">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
            <circle cx="12" cy="7" r="4"></circle>
          </svg>
          Entrar
        </router-link>

        <!-- Mobile Menu Button -->
        <button class="mobile-menu-btn" @click="toggleMenu">
          <svg
            v-if="!isMenuOpen"
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <line x1="3" y1="12" x2="21" y2="12"></line>
            <line x1="3" y1="6" x2="21" y2="6"></line>
            <line x1="3" y1="18" x2="21" y2="18"></line>
          </svg>
          <svg
            v-else
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      </div>
    </div>

    <!-- Mobile Menu -->
    <transition name="mobile-menu">
      <div v-if="isMenuOpen" class="mobile-menu">
        <nav class="mobile-nav">
          <router-link
            v-for="link in navLinks"
            :key="link.href"
            :to="link.href"
            class="mobile-nav-link"
            :class="{ active: isActive(link.href) }"
            @click="closeMenu"
          >
            {{ link.label }}
          </router-link>

          <div class="mobile-divider"></div>

          <router-link to="/login" class="mobile-btn-entrar" @click="closeMenu">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
              <circle cx="12" cy="7" r="4"></circle>
            </svg>
            Entrar
          </router-link>
        </nav>
      </div>
    </transition>
  </header>
</template>

<script setup>
import { ref} from 'vue';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();
const searchQuery = ref('');
const isMenuOpen = ref(false);

const navLinks = [
  { href: '/', label: 'Início' },
  { href: '/produtos', label: 'Produtos' },
  { href: '/categorias', label: 'Categorias' },
  { href: '/contato', label: 'Contato' },
];

const isActive = (path) => {
  return route.path === path;
};

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value;
};

const closeMenu = () => {
  isMenuOpen.value = false;
};

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
  width: 100%;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  background-color: rgba(24, 24, 24, 0.733);
  backdrop-filter: blur(10px);
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 64px;
  gap: var(--spacing-lg);
}

.logo {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  flex-shrink: 0;
}

.logo img {
  height: 40px;
  width: auto;
}

/* Desktop Navigation */
.nav {
  display: none;
  align-items: center;
  gap: var(--spacing-xl);
}

@media (min-width: 768px) {
  .nav {
    display: flex;
  }
}

.nav-link {
  color: var(--color-text-secondary);
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  transition: color var(--transition-fast);
  position: relative;
}

.nav-link:hover {
  color: var(--color-primary);
}

.nav-link.active {
  color: var(--color-primary);
}

/* Search Bar */
.search-bar {
  display: none;
  position: relative;
  flex: 1;
  max-width: 448px;
  margin: 0 var(--spacing-xl);
}

@media (min-width: 1024px) {
  .search-bar {
    display: flex;
  }
}

.search-icon {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--color-text-muted);
  pointer-events: none;
}

.search-bar input {
  width: 100%;
  padding: var(--spacing-sm) var(--spacing-md);
  padding-left: 40px;
  background-color: var(--color-bg-secondary);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: var(--radius-md);
  color: var(--color-text-primary);
  font-size: var(--text-sm);
  transition: all var(--transition-fast);
}

.search-bar input::placeholder {
  color: var(--color-text-muted);
}

.search-bar input:focus {
  outline: none;
  border-color: var(--color-primary);
}

/* Actions */
.header-actions {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.icon-btn {
  background: transparent;
  border: none;
  color: var(--color-text-primary);
  cursor: pointer;
  padding: var(--spacing-sm);
  border-radius: var(--radius-md);
  transition: all var(--transition-fast);
  display: none;
}

@media (min-width: 768px) {
  .icon-btn {
    display: flex;
  }
}

.icon-btn:hover {
  color: var(--color-primary);
}

.btn-entrar {
  display: none;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-sm) var(--spacing-lg);
  background-color: transparent;
  color: var(--color-text-primary);
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-fast);
}

@media (min-width: 768px) {
  .btn-entrar {
    display: inline-flex;
  }
}

.btn-entrar:hover {
  border-color: var(--color-primary);
  color: var(--color-primary);
}

/* Mobile Menu Button */
.mobile-menu-btn {
  display: flex;
  background: transparent;
  border: none;
  color: var(--color-text-primary);
  cursor: pointer;
  padding: var(--spacing-sm);
}

@media (min-width: 768px) {
  .mobile-menu-btn {
    display: none;
  }
}

/* Mobile Menu */
.mobile-menu {
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  background-color: var(--color-bg-primary);
}

@media (min-width: 768px) {
  .mobile-menu {
    display: none;
  }
}

.mobile-nav {
  padding: var(--spacing-lg) 0;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.mobile-nav-link {
  padding: var(--spacing-md) var(--spacing-lg);
  color: var(--color-text-primary);
  font-size: var(--text-base);
  border-radius: var(--radius-md);
  transition: all var(--transition-fast);
}

.mobile-nav-link:hover {
  background-color: var(--color-bg-secondary);
}

.mobile-nav-link.active {
  background-color: var(--color-primary);
  color: var(--color-bg-primary);
}

.mobile-divider {
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  margin: var(--spacing-sm) 0;
}

.mobile-btn-entrar {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-sm);
  width: 100%;
  padding: var(--spacing-md);
  background-color: transparent;
  color: var(--color-text-primary);
  font-size: var(--text-base);
  font-weight: var(--font-medium);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: var(--radius-md);
  transition: all var(--transition-fast);
}

.mobile-btn-entrar:hover {
  border-color: var(--color-primary);
  color: var(--color-primary);
}

/* Animations */
.mobile-menu-enter-active,
.mobile-menu-leave-active {
  transition: all 0.3s ease;
}

.mobile-menu-enter-from,
.mobile-menu-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>
