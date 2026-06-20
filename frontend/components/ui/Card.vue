<template>
  <div :class="cardClasses">
    <div v-if="$slots.header" class="border-b border-gray-200 pb-4 mb-4">
      <slot name="header" />
    </div>
    
    <slot />
    
    <div v-if="$slots.footer" class="border-t border-gray-200 pt-4 mt-4">
      <slot name="footer" />
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  padding?: 'none' | 'sm' | 'md' | 'lg'
  hoverable?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  padding: 'md',
  hoverable: false
})

const cardClasses = computed(() => {
  const base = 'bg-white rounded-card shadow-card transition-all duration-300 transform'
  
  const paddings = {
    none: 'p-0',
    sm: 'p-4',
    md: 'p-6',
    lg: 'p-8'
  }
  
  const hover = props.hoverable ? 'hover:shadow-xl hover:-translate-y-1 hover:scale-105 cursor-pointer' : ''
  
  return [base, paddings[props.padding], hover].join(' ')
})
</script>
