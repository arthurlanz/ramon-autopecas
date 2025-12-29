<template>
  <div class="dashboard-layout">
    <DashboardSidebar />

    <main class="dashboard-main">
      <div class="dashboard-header">
        <div>
          <router-link to="/dashboard/anunciador" class="back-link">
            ← Voltar para anúncios
          </router-link>
          <h1>Novo Anúncio</h1>
          <p>Crie um novo anúncio para o site e Mercado Livre</p>
        </div>
      </div>

      <form @submit.prevent="handleSubmit" class="product-form">
        <div class="form-grid">
          <!-- Left Column -->
          <div class="form-section">
            <h2>Informações do Produto</h2>

            <div class="form-group">
              <label for="title">Título do Anúncio *</label>
              <input
                id="title"
                v-model="form.title"
                type="text"
                placeholder="Ex: Pastilha de Freio Dianteira - Honda Civic 2016-2021"
                required
              />
            </div>

            <div class="form-row">
              <div class="form-group">
                <label for="category">Categoria *</label>
                <select id="category" v-model="form.category" required>
                  <option value="">Selecione...</option>
                  <option value="1">Freios</option>
                  <option value="2">Motor</option>
                  <option value="3">Suspensão</option>
                  <option value="4">Elétrica</option>
                  <option value="5">Filtros</option>
                  <option value="6">Escapamento</option>
                </select>
              </div>

              <div class="form-group">
                <label for="brand">Marca *</label>
                <input
                  id="brand"
                  v-model="form.brand"
                  type="text"
                  placeholder="Ex: Bosch, Fras-le"
                  required
                />
              </div>
            </div>

            <div class="form-group">
              <label for="description">Descrição *</label>
              <textarea
                id="description"
                v-model="form.description"
                rows="6"
                placeholder="Descreva o produto em detalhes..."
                required
              ></textarea>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label for="sku">SKU *</label>
                <input
                  id="sku"
                  v-model="form.sku"
                  type="text"
                  placeholder="Ex: PFD-HC-2021"
                  required
                />
              </div>

              <div class="form-group">
                <label for="price">Preço (R$) *</label>
                <input
                  id="price"
                  v-model="form.price"
                  type="number"
                  step="0.01"
                  placeholder="0,00"
                  required
                />
              </div>

              <div class="form-group">
                <label for="stock">Estoque *</label>
                <input
                  id="stock"
                  v-model="form.stock"
                  type="number"
                  placeholder="0"
                  required
                />
              </div>
            </div>
          </div>

          <!-- Right Column -->
          <div class="form-section">
            <h2>Imagens</h2>
            <p class="section-description">Adicione até 6 imagens do produto</p>

            <div class="image-upload">
              <div class="upload-area" @click="triggerFileInput">
                <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                  <polyline points="17 8 12 3 7 8"></polyline>
                  <line x1="12" y1="3" x2="12" y2="15"></line>
                </svg>
                <p>Arraste imagens ou clique para selecionar</p>
              </div>
              <input
                ref="fileInput"
                type="file"
                accept="image/*"
                multiple
                @change="handleFileUpload"
                style="display: none"
              />
            </div>

            <div v-if="uploadedImages.length > 0" class="uploaded-images">
              <div
                v-for="(image, index) in uploadedImages"
                :key="index"
                class="image-preview"
              >
                <img :src="image" alt="Preview" />
                <button
                  type="button"
                  class="remove-image"
                  @click="removeImage(index)"
                >
                  ×
                </button>
              </div>
            </div>

            <h2>Integração Mercado Livre</h2>

            <div class="form-group">
              <label class="checkbox-label">
                <input
                  v-model="form.publishToML"
                  type="checkbox"
                />
                <span>Publicar no ML</span>
              </label>
              <p class="help-text">
                O anúncio será publicado no Mercado Livre assim que aprovado.
                Vendas em qualquer plataforma atualizarão o estoque automaticamente.
              </p>
            </div>

            <div v-if="form.publishToML" class="ml-info">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="12" y1="16" x2="12" y2="12"></line>
                <line x1="12" y1="8" x2="12.01" y2="8"></line>
              </svg>
              <p>
                O anúncio será sincronizado automaticamente com o Mercado Livre.
                Após aprovação, o link do ML será gerado.
              </p>
            </div>
          </div>
        </div>

        <!-- Form Actions -->
        <div class="form-actions">
          <button type="button" class="btn-secondary" @click="saveDraft">
            Salvar Rascunho
          </button>
          <button type="submit" class="btn-primary" :disabled="loading">
            <span v-if="loading" class="loading"></span>
            <svg v-else xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
              <polyline points="7 10 12 15 17 10"></polyline>
              <line x1="12" y1="15" x2="12" y2="3"></line>
            </svg>
            Publicar
          </button>
        </div>
      </form>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useProductsStore } from '../stores/products';
import DashboardSidebar from '../components/layout/DashboardSidebar.vue';

const router = useRouter();
const productsStore = useProductsStore();

const form = ref({
  title: '',
  category: '',
  brand: '',
  description: '',
  sku: '',
  price: '',
  stock: '',
  publishToML: true,
});

const uploadedImages = ref([]);
const fileInput = ref(null);
const loading = ref(false);

const triggerFileInput = () => {
  fileInput.value.click();
};

const handleFileUpload = (event) => {
  const files = Array.from(event.target.files);

  files.forEach((file) => {
    if (uploadedImages.value.length < 6) {
      const reader = new FileReader();
      reader.onload = (e) => {
        uploadedImages.value.push(e.target.result);
      };
      reader.readAsDataURL(file);
    }
  });
};

const removeImage = (index) => {
  uploadedImages.value.splice(index, 1);
};

const saveDraft = () => {
  alert('Rascunho salvo!');
};

const handleSubmit = async () => {
  loading.value = true;

  const formData = new FormData();
  Object.keys(form.value).forEach((key) => {
    formData.append(key, form.value[key]);
  });

  // Add images to formData
  uploadedImages.value.forEach((image, index) => {
    formData.append(`image_${index}`, image);
  });

  const result = await productsStore.createProduct(formData);

  if (result.success) {
    alert('Produto criado com sucesso!');
    router.push('/dashboard/anunciador');
  } else {
    alert('Erro ao criar produto');
  }

  loading.value = false;
};
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
