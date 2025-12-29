<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-card">
        <router-link to="/" class="logo">
          <img src="C:\Users\arthu\Documents\ramon-autopecas\frontend\src\assets\logo.png" alt="Ramon Autopeças" />
        </router-link>

        <h1>Bem-vindo de volta</h1>
        <p class="subtitle">Entre com suas credenciais para acessar o sistema</p>

        <form @submit.prevent="handleLogin">
          <div class="form-group">
            <label for="username">Usuário</label>
            <input
              id="username"
              v-model="credentials.username"
              type="text"
              placeholder="Digite seu usuário"
              required
            />
          </div>

          <div class="form-group">
            <label for="password">Senha</label>
            <input
              id="password"
              v-model="credentials.password"
              type="password"
              placeholder="Digite sua senha"
              required
            />
          </div>

          <div v-if="errorMessage" class="error-message">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="12" y1="8" x2="12" y2="12"></line>
              <line x1="12" y1="16" x2="12.01" y2="16"></line>
            </svg>
            {{ errorMessage }}
          </div>

          <button type="submit" class="btn-primary btn-full" :disabled="loading">
            <span v-if="loading" class="loading"></span>
            <span v-else>Entrar</span>
          </button>
        </form>

        <div class="login-footer">
          <router-link to="/">← Voltar para o site</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';

const router = useRouter();
const authStore = useAuthStore();

const credentials = ref({
  username: '',
  password: '',
});

const errorMessage = ref('');
const loading = ref(false);

const handleLogin = async () => {
  errorMessage.value = '';
  loading.value = true;

  try {
    const result = await authStore.login(
      credentials.value.username,
      credentials.value.password
    );

    if (result.success) {
      const redirectPath = authStore.isOwner
        ? '/dashboard/dono'
        : '/dashboard/anunciador';

      router.push(redirectPath);
    } else {
      errorMessage.value = result.message || 'Credenciais inválidas';
    }
  } catch (err) {
    console.error('Erro ao fazer login:', err);
    errorMessage.value = 'Erro ao fazer login. Tente novamente.';
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--color-bg-primary) 0%, var(--color-bg-secondary) 100%);
  padding: var(--spacing-xl);
}

.login-container {
  width: 100%;
  max-width: 450px;
}

.login-card {
  background-color: var(--color-bg-card);
  border-radius: var(--radius-xl);
  padding: var(--spacing-3xl);
  box-shadow: var(--shadow-xl);
}

.logo {
  display: block;
  text-align: center;
  margin-bottom: var(--spacing-2xl);
}

.logo img {
  height: 50px;
  width: auto;
}

h1 {
  font-size: var(--text-3xl);
  font-weight: var(--font-black);
  text-align: center;
  margin-bottom: var(--spacing-sm);
}

.subtitle {
  text-align: center;
  color: var(--color-text-secondary);
  margin-bottom: var(--spacing-2xl);
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

.error-message {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-md);
  background-color: rgba(220, 38, 38, 0.1);
  border: 1px solid var(--color-error);
  border-radius: var(--radius-md);
  color: var(--color-error);
  font-size: var(--text-sm);
  margin-bottom: var(--spacing-lg);
}

.btn-full {
  width: 100%;
  justify-content: center;
}

.login-footer {
  margin-top: var(--spacing-xl);
  text-align: center;
}

.login-footer a {
  color: var(--color-text-secondary);
  font-size: var(--text-sm);
}

.login-footer a:hover {
  color: var(--color-primary);
}
</style>
