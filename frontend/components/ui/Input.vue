<template>
  <div class="relative">
    <label
      v-if="label"
      :for="id"
      class="block text-sm font-medium text-primary-charcoal mb-2"
    >
      {{ label }}
      <span v-if="required" class="text-primary-red ml-1">*</span>
    </label>
    
    <input
      :id="id"
      :type="type"
      :value="modelValue"
      :placeholder="placeholder"
      :disabled="disabled"
      :required="required"
      :class="inputClasses"
      @input="handleInput"
      @blur="handleBlur"
    />
    
    <p v-if="error" class="mt-1 text-sm text-primary-red">{{ error }}</p>
    <p v-if="hint && !error" class="mt-1 text-sm text-gray-500">{{ hint }}</p>
  </div>
</template>

<script setup lang="ts">
interface Props {
  id?: string
  label?: string
  type?: string
  modelValue?: string | number
  placeholder?: string
  disabled?: boolean
  required?: boolean
  error?: string
  hint?: string
}

const props = withDefaults(defineProps<Props>(), {
  type: 'text',
  disabled: false,
  required: false
})

const emit = defineEmits<{
  'update:modelValue': [value: string | number]
  blur: [event: FocusEvent]
}>()

const handleInput = (event: Event) => {
  const target = event.target as HTMLInputElement
  emit('update:modelValue', target.value)
}

const handleBlur = (event: FocusEvent) => {
  emit('blur', event)
}

const inputClasses = computed(() => {
  const base = 'w-full px-4 py-3 border rounded-lg transition-all focus:outline-none focus:ring-2'
  
  const errorState = props.error
    ? 'border-primary-red focus:ring-primary-red'
    : 'border-gray-300 focus:ring-primary-gold focus:border-transparent'
  
  const disabled = props.disabled ? 'bg-gray-100 cursor-not-allowed' : 'bg-white'
  
  return [base, errorState, disabled].join(' ')
})
</script>
