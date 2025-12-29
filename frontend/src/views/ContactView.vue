<template>
  <div class="contact-page">
    <HeaderComponent />

    <div class="container page-content">
      <div class="page-header">
        <h1>Contato</h1>
        <p>Entre em contato conosco</p>
      </div>

      <div class="contact-content">
        <!-- Contact Info -->
        <div class="contact-info">
          <h2>Informações de Contato</h2>

          <div class="info-item">
            <div class="info-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
                <circle cx="12" cy="10" r="3"></circle>
              </svg>
            </div>
            <div>
              <h3>Endereço</h3>
              <p>Rua das Autopeças, 123 Centro<br />São Paulo, SP - CEP 01000-000</p>
            </div>
          </div>

          <div class="info-item">
            <div class="info-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path>
              </svg>
            </div>
            <div>
              <h3>Telefone</h3>
              <p>(11) 99999-9999<br />(11) 3333-3333</p>
            </div>
          </div>

          <div class="info-item">
            <div class="info-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="2" y="4" width="20" height="16" rx="2"></rect>
                <path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"></path>
              </svg>
            </div>
            <div>
              <h3>E-mail</h3>
              <p>contato@ramonautopecas.com.br<br />vendas@ramonautopecas.com.br</p>
            </div>
          </div>

          <div class="info-item">
            <div class="info-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"></circle>
                <polyline points="12 6 12 12 16 14"></polyline>
              </svg>
            </div>
            <div>
              <h3>Horário de Funcionamento</h3>
              <p>Segunda a Sexta: 8h às 18h<br />Sábado: 8h às 13h</p>
            </div>
          </div>
        </div>

        <!-- Contact Form -->
        <div class="contact-form">
          <h2>Envie uma Mensagem</h2>

          <form @submit.prevent="handleSubmit">
            <div class="form-group">
              <label for="name">Nome</label>
              <input
                id="name"
                v-model="form.name"
                type="text"
                placeholder="Seu nome completo"
                required
              />
            </div>

            <div class="form-group">
              <label for="email">E-mail</label>
              <input
                id="email"
                v-model="form.email"
                type="email"
                placeholder="seu@email.com"
                required
              />
            </div>

            <div class="form-group">
              <label for="phone">Telefone</label>
              <input
                id="phone"
                v-model="form.phone"
                type="tel"
                placeholder="(11) 99999-9999"
              />
            </div>

            <div class="form-group">
              <label for="subject">Assunto</label>
              <input
                id="subject"
                v-model="form.subject"
                type="text"
                placeholder="Qual o motivo do contato?"
                required
              />
            </div>

            <div class="form-group">
              <label for="message">Mensagem</label>
              <textarea
                id="message"
                v-model="form.message"
                rows="6"
                placeholder="Digite sua mensagem..."
                required
              ></textarea>
            </div>

            <div v-if="successMessage" class="success-message">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              {{ successMessage }}
            </div>

            <button type="submit" class="btn-primary" :disabled="loading">
              <span v-if="loading" class="loading"></span>
              <span v-else>Enviar Mensagem</span>
            </button>
          </form>
        </div>
      </div>
    </div>

    <FooterComponent />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import HeaderComponent from '../components/layout/HeaderComponent.vue';
import FooterComponent from '../components/layout/FooterComponent.vue';

const form = ref({
  name: '',
  email: '',
  phone: '',
  subject: '',
  message: '',
});

const loading = ref(false);
const successMessage = ref('');

const handleSubmit = async () => {
  loading.value = true;
  successMessage.value = '';

  // Simular envio (substituir por API real)
  setTimeout(() => {
    successMessage.value = 'Mensagem enviada com sucesso! Entraremos em contato em breve.';
    form.value = {
      name: '',
      email: '',
      phone: '',
      subject: '',
      message: '',
    };
    loading.value = false;
  }, 1500);
};
</script>

<style scoped>
.contact-page {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.page-content {
  padding: var(--spacing-3xl) var(--spacing-xl);
  flex: 1;
}

.page-header {
  text-align: center;
  margin-bottom: var(--spacing-3xl);
}

.page-header h1 {
  margin-bottom: var(--spacing-sm);
}

.page-header p {
  color: var(--color-text-secondary);
  font-size: var(--text-lg);
}

.contact-content {
  display: grid;
  grid-template-columns: 1fr 1.5fr;
  gap: var(--spacing-3xl);
}

.contact-info h2,
.contact-form h2 {
  font-size: var(--text-2xl);
  margin-bottom: var(--spacing-xl);
}

.info-item {
  display: flex;
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-xl);
}

.info-icon {
  width: 50px;
  height: 50px;
  flex-shrink: 0;
  background-color: rgba(253, 184, 19, 0.2);
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
}

.info-icon svg {
  color: var(--color-primary);
}

.info-item h3 {
  font-size: var(--text-lg);
  margin-bottom: var(--spacing-xs);
}

.info-item p {
  color: var(--color-text-secondary);
  line-height: 1.6;
}

.contact-form {
  background-color: var(--color-bg-card);
  padding: var(--spacing-2xl);
  border-radius: var(--radius-lg);
}

.form-group {
  margin-bottom: var(--spacing-lg);
}

.form-group label {
  display: block;
  font-size: var(--text-sm);
  font-weight: var(--font-semibold);
  color: var(--color-text-secondary);
  margin-bottom: var(--spacing-sm);
}

.success-message {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-md);
  background-color: rgba(16, 185, 129, 0.1);
  border: 1px solid var(--color-success);
  border-radius: var(--radius-md);
  color: var(--color-success);
  font-size: var(--text-sm);
  margin-bottom: var(--spacing-lg);
}

@media (max-width: 968px) {
  .contact-content {
    grid-template-columns: 1fr;
  }
}
</style>
