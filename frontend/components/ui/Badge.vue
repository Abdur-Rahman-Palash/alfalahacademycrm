<template>
  <span :class="badgeClasses">
    <slot />
  </span>
</template>

<script setup lang="ts">
interface Props {
  variant?: 'success' | 'warning' | 'danger' | 'info' | 'neutral'
  size?: 'sm' | 'md'
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'neutral',
  size: 'md'
})

const badgeClasses = computed(() => {
  const base = 'inline-flex items-center px-3 py-1 rounded-full font-medium'
  
  const variants = {
    success: 'bg-green-100 text-green-800',
    warning: 'bg-yellow-100 text-yellow-800',
    danger: 'bg-red-100 text-red-800',
    info: 'bg-blue-100 text-blue-800',
    neutral: 'bg-gray-100 text-gray-800'
  }
  
  const sizes = {
    sm: 'text-xs',
    md: 'text-sm'
  }
  
  return [base, variants[props.variant], sizes[props.size]].join(' ')
})
</script>
