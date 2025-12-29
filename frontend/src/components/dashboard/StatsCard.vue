<template>
  <div class="stats-card" :style="{ backgroundColor: bgColor }">
    <div class="stats-content">
      <div class="stats-info">
        <p class="stats-label">{{ label }}</p>
        <h3 class="stats-value">{{ formattedValue }}</h3>
        <p v-if="change" class="stats-change" :class="changeClass">
          {{ change }}
        </p>
      </div>
      <div class="stats-icon" :style="{ backgroundColor: iconBgColor }">
        <slot name="icon"></slot>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  label: {
    type: String,
    required: true,
  },
  value: {
    type: [Number, String],
    required: true,
  },
  type: {
    type: String,
    default: 'default', // 'default', 'currency', 'percentage'
  },
  change: {
    type: String,
    default: null,
  },
  bgColor: {
    type: String,
    default: 'var(--color-card-products)',
  },
  iconBgColor: {
    type: String,
    default: 'var(--color-primary)',
  },
});

const formattedValue = computed(() => {
  if (props.type === 'currency') {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL',
    }).format(props.value);
  }
  if (props.type === 'percentage') {
    return `${props.value}%`;
  }
  return props.value;
});

const changeClass = computed(() => {
  if (!props.change) return '';
  return props.change.includes('+') ? 'positive' : 'negative';
});
</script>

<style scoped>
.stats-card {
  border-radius: var(--radius-lg);
  padding: var(--spacing-xl);
  transition: all var(--transition-base);
}

.stats-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-xl);
}

.stats-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.stats-info {
  flex: 1;
}

.stats-label {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  margin-bottom: var(--spacing-xs);
}

.stats-value {
  font-size: var(--text-4xl);
  font-weight: var(--font-black);
  color: var(--color-text-primary);
  margin: 0;
  line-height: 1;
}

.stats-change {
  font-size: var(--text-xs);
  font-weight: var(--font-semibold);
  margin-top: var(--spacing-sm);
}

.stats-change.positive {
  color: var(--color-success);
}

.stats-change.negative {
  color: var(--color-error);
}

.stats-icon {
  width: 60px;
  height: 60px;
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stats-icon :deep(svg) {
  width: 30px;
  height: 30px;
  color: var(--color-bg-primary);
}

@media (max-width: 768px) {
  .stats-value {
    font-size: var(--text-3xl);
  }

  .stats-icon {
    width: 50px;
    height: 50px;
  }

  .stats-icon :deep(svg) {
    width: 24px;
    height: 24px;
  }
}
</style>
