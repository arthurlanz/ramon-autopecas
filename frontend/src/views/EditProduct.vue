<template>
  <div class="dashboard-layout">
    <DashboardSidebar />

    <main class="dashboard-main">
      <div v-if="loading" class="loading-container">
        <div class="loading"></div>
        <p>Carregando produto...</p>
      </div>

      <div v-else-if="product">
        <div class="dashboard-header">
          <div>
            <router-link to="/dashboard/anunciador" class="back-link">
              ← Voltar para anúncios
            </router-link>
            <h1>Editar Anúncio</h1>
            <p>{{ product.title }}</p>
          </div>
        </div>

        <!-- Same form as NewProduct but with pre-filled data -->
        <form @submit.prevent="handleUpdate" class="product-form">
          <!-- Copy the entire form from NewProduct.vue here with v-model bound to product data -->
          <p style="color: var(--color-text-secondary); text-align: center; padding: var(--spacing-3xl);">
            Formulário de edição (copiar estrutura do NewProduct.vue e preencher com dados do produto)
          </p>

          <div class="form-actions">
            <button type="button" class="btn-secondary" @click="$router.back()">
              Cancelar
            </button>
            <button type="submit" class="btn-primary" :disabled="updating">
              <span v-if="updating" class="loading"></span>
              <span v-else>Salvar Alterações</span>
            </button>
          </div>
        </form>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useProductsStore } from '../stores/products';
import DashboardSidebar from '../components/layout/DashboardSidebar.vue';

const route = useRoute();
const router = useRouter();
const productsStore = useProductsStore();

const product = ref(null);
const loading = ref(true);
const updating = ref(false);

const handleUpdate = async () => {
  updating.value = true;

  const result = await productsStore.updateProduct(product.value.id, product.value);

  if (result.success) {
    alert('Produto atualizado com sucesso!');
    router.push('/dashboard/anunciador');
  } else {
    alert('Erro ao atualizar produto');
  }

  updating.value = false;
};

onMounted(async () => {
  try {
    product.value = await productsStore.fetchProductById(route.params.id);
  } catch (error) {
    console.error('Erro ao carregar produto:', error);
    router.push('/dashboard/anunciador');
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>.dashboard-layout {
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
  margin-bottom: var(--spacing-2xl);
}

.back-link {
  display: inline-block;
  color: var(--color-text-secondary);
  font-size: var(--text-sm);
  margin-bottom: var(--spacing-md);
}

.back-link:hover {
  color: var(--color-primary);
}

.dashboard-header h1 {
  font-size: var(--text-3xl);
  margin-bottom: var(--spacing-xs);
}

.dashboard-header p {
  color: var(--color-text-secondary);
}

.product-form {
  background-color: var(--color-bg-card);
  border-radius: var(--radius-lg);
  padding: var(--spacing-2xl);
}

.form-grid {
  display: grid;
  grid-template-columns: 1.5fr 1fr;
  gap: var(--spacing-3xl);
  margin-bottom: var(--spacing-2xl);
}

.form-section h2 {
  font-size: var(--text-xl);
  font-weight: var(--font-black);
  text-transform: uppercase;
  margin-bottom: var(--spacing-lg);
}

.section-description {
  color: var(--color-text-secondary);
  font-size: var(--text-sm);
  margin-bottom: var(--spacing-lg);
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

.form-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: var(--spacing-md);
}

.image-upload {
  margin-bottom: var(--spacing-xl);
}

.upload-area {
  border: 2px dashed var(--color-text-muted);
  border-radius: var(--radius-lg);
  padding: var(--spacing-3xl);
  text-align: center;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.upload-area:hover {
  border-color: var(--color-primary);
  background-color: rgba(253, 184, 19, 0.05);
}

.upload-area svg {
  color: var(--color-text-muted);
  margin-bottom: var(--spacing-md);
}

.upload-area p {
  color: var(--color-text-secondary);
  margin: 0;
}

.uploaded-images {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--spacing-md);
}

.image-preview {
  position: relative;
  aspect-ratio: 1;
  border-radius: var(--radius-md);
  overflow: hidden;
}

.image-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.remove-image {
  position: absolute;
  top: var(--spacing-sm);
  right: var(--spacing-sm);
  width: 30px;
  height: 30px;
  background-color: var(--color-error);
  border: none;
  border-radius: 50%;
  color: white;
  font-size: var(--text-xl);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  cursor: pointer;
  font-weight: var(--font-semibold);
}

.checkbox-label input {
  width: auto;
}

.help-text {
  font-size: var(--text-sm);
  color: var(--color-text-muted);
  margin: var(--spacing-sm) 0 0;
}

.ml-info {
  display: flex;
  gap: var(--spacing-md);
  padding: var(--spacing-md);
  background-color: rgba(253, 184, 19, 0.1);
  border: 1px solid var(--color-primary);
  border-radius: var(--radius-md);
  margin-top: var(--spacing-lg);
}

.ml-info svg {
  flex-shrink: 0;
  color: var(--color-primary);
  margin-top: 2px;
}

.ml-info p {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  margin: 0;
}

.form-actions {
  display: flex;
  gap: var(--spacing-md);
  justify-content: flex-end;
  padding-top: var(--spacing-xl);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

@media (max-width: 968px) {
  .dashboard-main {
    margin-left: 70px;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }
}
</style>
