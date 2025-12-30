<template>
  <section class="hero-section">
    <!-- Background -->
    <div class="hero-bg"></div>
    <div class="hero-blobs">
      <div class="blob blob-1"></div>
      <div class="blob blob-2"></div>
    </div>

    <div class="container hero-container">
      <div class="hero-content">
        <h1 class="hero-title">
          PEÇAS DE <span class="text-gradient">QUALIDADE</span> PARA SEU VEÍCULO
        </h1>
        <p class="hero-description">
          Encontre as melhores peças automotivas com preços imbatíveis.
          Qualidade garantida e entrega rápida para todo o Brasil.
        </p>
        <div class="hero-actions">
          <router-link to="/produtos" class="btn-hero">
            Ver Produtos
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <line x1="5" y1="12" x2="19" y2="12"></line>
              <polyline points="12 5 19 12 12 19"></polyline>
            </svg>
          </router-link>
          <a :href="mlStoreUrl" target="_blank" rel="noopener noreferrer" class="btn-ml">
            Nossa Loja no ML
          </a>
        </div>
      </div>

      <!-- Features -->
      <div class="features-grid">
        <div
          v-for="(feature, index) in features"
          :key="feature.title"
          class="feature-item"
          :style="{ animationDelay: `${0.3 + index * 0.1}s` }"
        >
          <div class="feature-icon">
            <div v-html="feature.icon"></div>
          </div>
          <div class="feature-text">
            <h3>{{ feature.title }}</h3>
            <p>{{ feature.description }}</p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue';

const mlStoreUrl = import.meta.env.VITE_ML_STORE_URL || 'https://www.mercadolivre.com.br';

const features = ref([
  {
    title: 'Entrega Rápida',
    description: 'Enviamos para todo o Brasil',
    icon: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <rect x="1" y="3" width="15" height="13"></rect>
      <polygon points="16 8 20 8 23 11 23 16 16 16 16 8"></polygon>
      <circle cx="5.5" cy="18.5" r="2.5"></circle>
      <circle cx="18.5" cy="18.5" r="2.5"></circle>
    </svg>`,
  },
  {
    title: 'Garantia',
    description: 'Todos os produtos com garantia',
    icon: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
    </svg>`,
  },
  {
    title: 'Parcelamento',
    description: 'Em até 12x sem juros',
    icon: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <rect x="1" y="4" width="22" height="16" rx="2" ry="2"></rect>
      <line x1="1" y1="10" x2="23" y2="10"></line>
    </svg>`,
  },
]);
</script>

<style scoped>
.hero-section {
  position: relative;
  overflow: hidden;
  padding: 80px 0 64px;
}

@media (min-width: 1024px) {
  .hero-section {
    padding: 128px 0;
  }
}

/* Background */
.hero-bg {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, var(--color-bg-primary) 0%, var(--color-bg-secondary) 50%, var(--color-bg-secondary) 200%);
}

.hero-blobs {
  position: absolute;
  inset: 0;
  opacity: 0.2;
  pointer-events: none;
}

.blob {
  position: absolute;
  border-radius: 50%;
  filter: blur(60px);
  animation: float 8s ease-in-out infinite;
}

.blob-1 {
  top: 80px;
  left: 40px;
  width: 288px;
  height: 288px;
  background-color: rgba(253, 184, 19, 0.3);
}

.blob-2 {
  bottom: 80px;
  right: 40px;
  width: 384px;
  height: 384px;
  background-color: rgba(253, 184, 19, 0.2);
  animation-delay: -4s;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-20px);
  }
}

/* Container */
.hero-container {
  position: relative;
  z-index: 1;
}

.hero-content {
  max-width: 768px;
  margin: 0 auto;
  text-align: center;
}

/* Title */
.hero-title {
  font-size: clamp(1rem, 7vw, 4rem);
  font-weight: var(--font-black);
  line-height: 1.1;
  margin-bottom: var(--spacing-xl);
  color: var(--color-text-primary);
  animation: fadeIn 0.6s ease-out;
}

.text-gradient {
  background: linear-gradient(135deg, var(--color-primary) 0%, #e5a610 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Description */
.hero-description {
  font-size: clamp(1rem, 2vw, 1.25rem);
  color: var(--color-text-secondary);
  margin-bottom: var(--spacing-2xl);
  line-height: 1.6;
  animation: fadeIn 0.6s ease-out 0.1s backwards;
}

/* Actions */
.hero-actions {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
  justify-content: center;
  animation: fadeIn 0.6s ease-out 0.2s backwards;
  margin-bottom: var(--spacing-3xl);
}

@media (min-width: 640px) {
  .hero-actions {
    flex-direction: row;
  }
}

.btn-ml {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-sm);
  padding: 16px 32px;
  background-color: var(--color-primary);
  color: var(--color-bg-primary);
  font-size: var(--text-lg);
  font-weight: var(--font-bold);
  border-radius: var(--radius-lg);
  transition: all var(--transition-base);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border: none;
  cursor: pointer;
}

.btn-ml:hover {
  background-color: liner-gradient(135deg, #e5a610 0%, #fdb813 100%);
  transform: translateY(-2px);
}

.btn-hero {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 16px 32px;
  background-color: var(--color-primary);
  color: var(--color-bg-primary);
  font-size: var(--text-lg);
  font-weight: var(--font-bold);
  border-radius: var(--radius-lg);
  transition: all var(--transition-base);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.btn-hero:hover {
  background-color: var(--color-primary);
  transform: translateY(-2px);
}

/* Features Grid */
.features-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--spacing-lg);
  margin-top: var(--spacing-3xl);
}

@media (min-width: 768px) {
  .features-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

.feature-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-xl);
  border-radius: var(--radius-xl);
  background-color: rgba(31, 31, 31, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  transition: all var(--transition-base);
  animation: fadeIn 0.6s ease-out backwards;
}

.feature-item:hover {
  transform: translateY(-4px);
  border-color: rgba(253, 184, 19, 0.3);
  box-shadow: var(--shadow-lg);
}

.feature-icon {
  width: 48px;
  height: 48px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-lg);
  background-color: rgba(253, 184, 19, 0.1);
}

.feature-icon :deep(svg) {
  color: var(--color-primary);
  width: 24px;
  height: 24px;
}

.feature-text h3 {
  font-size: var(--text-base);
  font-weight: var(--font-semibold);
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-xs);
}

.feature-text p {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  margin: 0;
}

/* Animations */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
