<template>
  <footer class="footer">
    <div class="container">
      <div class="footer-content">
        <!-- About Section -->
        <div class="footer-section">
          <img src="C:\Users\arthu\Documents\ramon-autopecas\frontend\src\assets\logo.png" alt="Ramon Autopeças" class="footer-logo" />
          <p class="footer-description">
            Sua loja de autopeças de confiança. Qualidade e preço justo para manter seu veículo sempre em dia.
          </p>
          <div class="social-links">
            <a href="#" class="social-icon" aria-label="Facebook">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
              </svg>
            </a>
            <a href="#" class="social-icon" aria-label="Instagram">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect>
                <path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path>
                <line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line>
              </svg>
            </a>
          </div>
        </div>

        <!-- Quick Links -->
        <div class="footer-section">
          <h3 class="footer-title">Links Rápidos</h3>
          <ul class="footer-links">
            <li><router-link to="/">Início</router-link></li>
            <li><router-link to="/produtos">Produtos</router-link></li>
            <li><router-link to="/categorias">Categorias</router-link></li>
            <li><router-link to="/contato">Sobre Nós</router-link></li>
            <li><router-link to="/contato">Contato</router-link></li>
          </ul>
        </div>

        <!-- Categories -->
        <div class="footer-section">
          <h3 class="footer-title">Categorias</h3>
          <ul class="footer-links">
            <li><a href="#">Freios</a></li>
            <li><a href="#">Motor</a></li>
            <li><a href="#">Suspensão</a></li>
            <li><a href="#">Elétrica</a></li>
            <li><a href="#">Filtros</a></li>
            <li><a href="#">Escapamento</a></li>
          </ul>
        </div>

        <!-- Contact -->
        <div class="footer-section">
          <h3 class="footer-title">Contato</h3>
          <ul class="footer-contact">
            <li>
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
                <circle cx="12" cy="10" r="3"></circle>
              </svg>
              <span>Rua das Autopeças, 123 Centro - São Paulo, SP</span>
            </li>
            <li>
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path>
              </svg>
              <span>(11) 99999-9999</span>
            </li>
            <li>
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="2" y="4" width="20" height="16" rx="2"></rect>
                <path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"></path>
              </svg>
              <span>contato@ramonautopecas.com.br</span>
            </li>
            <li>
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"></circle>
                <polyline points="12 6 12 12 16 14"></polyline>
              </svg>
              <span>Seg-Sex: 8h-18h | Sáb: 8h-13h</span>
            </li>
          </ul>
        </div>
      </div>

      <!-- Bottom Bar -->
      <div class="footer-bottom">
        <p>© 2024 Ramon Autopeças. Todos os direitos reservados.</p>
        <p>
          Vendemos também no
          <a :href="mlStoreUrl" target="_blank" rel="noopener noreferrer">
            Mercado Livre
          </a>
        </p>
      </div>
    </div>
  </footer>
</template>

<script setup>
const mlStoreUrl = import.meta.env.VITE_ML_STORE_URL;
</script>

<style scoped>
.footer {
  background-color: var(--color-bg-secondary);
  padding: var(--spacing-3xl) 0 var(--spacing-xl);
  margin-top: var(--spacing-3xl);
}

.footer-content {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1.5fr;
  gap: var(--spacing-2xl);
  margin-bottom: var(--spacing-2xl);
}

.footer-section {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.footer-logo {
  height: 90px;
  width: 90px;
  margin-bottom: var(--spacing-sm);
}

.footer-description {
  color: var(--color-text-secondary);
  font-size: var(--text-sm);
  line-height: 1.6;
  margin: 0;
}

.social-links {
  display: flex;
  gap: var(--spacing-md);
  margin-top: var(--spacing-sm);
}

.social-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--color-bg-primary);
  border-radius: var(--radius-md);
  color: var(--color-text-secondary);
  transition: all var(--transition-fast);
}

.social-icon:hover {
  background-color: var(--color-primary);
  color: var(--color-bg-primary);
  transform: translateY(-3px);
}

.footer-title {
  font-size: var(--text-lg);
  font-weight: var(--font-bold);
  color: var(--color-text-primary);
  text-transform: uppercase;
  margin-bottom: var(--spacing-sm);
}

.footer-links,
.footer-contact {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.footer-links a {
  color: var(--color-text-secondary);
  font-size: var(--text-sm);
  transition: color var(--transition-fast);
}

.footer-links a:hover {
  color: var(--color-primary);
}

.footer-contact li {
  display: flex;
  align-items: flex-start;
  gap: var(--spacing-sm);
  color: var(--color-text-secondary);
  font-size: var(--text-sm);
}

.footer-contact svg {
  flex-shrink: 0;
  color: var(--color-primary);
  margin-top: 2px;
}

.footer-bottom {
  padding-top: var(--spacing-xl);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: var(--spacing-md);
}

.footer-bottom p {
  color: var(--color-text-muted);
  font-size: var(--text-sm);
  margin: 0;
}

.footer-bottom a {
  color: var(--color-primary);
  font-weight: var(--font-semibold);
}

@media (max-width: 1024px) {
  .footer-content {
    grid-template-columns: 1fr 1fr;
  }
}

@media (max-width: 640px) {
  .footer-content {
    grid-template-columns: 1fr;
  }

  .footer-bottom {
    flex-direction: column;
    text-align: center;
  }
}
</style>
