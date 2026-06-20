<template>
  <div class="stripe-payment-form">
    <div v-if="loading" class="flex items-center justify-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-gold"></div>
    </div>
    
    <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
      <p class="text-red-600">{{ error }}</p>
    </div>
    
    <form v-else @submit.prevent="handleSubmit" class="space-y-6">
      <!-- Donation Amount -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Donation Amount</label>
        <div class="grid grid-cols-4 gap-3 mb-3">
          <button
            v-for="amount in presetAmounts"
            :key="amount"
            type="button"
            @click="selectAmount(amount)"
            :class="[
              'py-3 px-4 rounded-lg border-2 transition-all duration-200 font-medium',
              selectedAmount === amount
                ? 'border-primary-gold bg-primary-gold text-white'
                : 'border-gray-200 hover:border-primary-gold text-gray-700'
            ]"
          >
            ${{ amount }}
          </button>
        </div>
        <div class="relative">
          <span class="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-500 font-medium">$</span>
          <input
            v-model="customAmount"
            type="number"
            placeholder="Custom amount"
            class="w-full pl-8 pr-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-gold focus:border-transparent"
            @input="clearPreset"
          />
        </div>
      </div>

      <!-- Recurring Donation -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Make this a recurring donation</label>
        <div class="grid grid-cols-3 gap-3">
          <button
            v-for="frequency in frequencies"
            :key="frequency.value"
            type="button"
            @click="selectFrequency(frequency.value)"
            :class="[
              'py-3 px-4 rounded-lg border-2 transition-all duration-200 font-medium',
              selectedFrequency === frequency.value
                ? 'border-primary-gold bg-primary-gold text-white'
                : 'border-gray-200 hover:border-primary-gold text-gray-700'
            ]"
          >
            {{ frequency.label }}
          </button>
        </div>
      </div>

      <!-- Donor Information -->
      <div class="space-y-4">
        <h3 class="text-lg font-semibold text-primary-navy">Donor Information</h3>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">First Name *</label>
            <input
              v-model="formData.firstName"
              type="text"
              required
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-gold focus:border-transparent"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Last Name *</label>
            <input
              v-model="formData.lastName"
              type="text"
              required
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-gold focus:border-transparent"
            />
          </div>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Email *</label>
          <input
            v-model="formData.email"
            type="email"
            required
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-gold focus:border-transparent"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Phone</label>
          <input
            v-model="formData.phone"
            type="tel"
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-gold focus:border-transparent"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Address</label>
          <input
            v-model="formData.address"
            type="text"
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-gold focus:border-transparent"
          />
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">City</label>
            <input
              v-model="formData.city"
              type="text"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-gold focus:border-transparent"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">State</label>
            <input
              v-model="formData.state"
              type="text"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-gold focus:border-transparent"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">ZIP Code</label>
            <input
              v-model="formData.zip"
              type="text"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-gold focus:border-transparent"
            />
          </div>
        </div>
      </div>

      <!-- Payment Method -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Payment Information</label>
        <div id="card-element" class="p-4 border border-gray-300 rounded-lg bg-white"></div>
      </div>

      <!-- Dedication -->
      <div>
        <label class="flex items-center space-x-2">
          <input
            v-model="formData.isDedication"
            type="checkbox"
            class="w-4 h-4 text-primary-gold rounded focus:ring-primary-gold"
          />
          <span class="text-sm font-medium text-gray-700">Dedicate this donation</span>
        </label>
        
        <div v-if="formData.isDedication" class="mt-4 space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Dedication Type</label>
            <select
              v-model="formData.dedicationType"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-gold focus:border-transparent"
            >
              <option value="in_memory">In Memory Of</option>
              <option value="in_honor">In Honor Of</option>
              <option value="tribute">Tribute</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Dedication Name</label>
            <input
              v-model="formData.dedicationName"
              type="text"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-gold focus:border-transparent"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Notify Recipient (Email)</label>
            <input
              v-model="formData.dedicationEmail"
              type="email"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-gold focus:border-transparent"
            />
          </div>
        </div>
      </div>

      <!-- Campaign Selection -->
      <div v-if="campaigns.length > 0">
        <label class="block text-sm font-medium text-gray-700 mb-2">Apply to Campaign</label>
        <select
          v-model="formData.campaignId"
          class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-gold focus:border-transparent"
        >
          <option value="">General Donation</option>
          <option v-for="campaign in campaigns" :key="campaign.id" :value="campaign.id">
            {{ campaign.name }}
          </option>
        </select>
      </div>

      <!-- Anonymous Donation -->
      <div>
        <label class="flex items-center space-x-2">
          <input
            v-model="formData.isAnonymous"
            type="checkbox"
            class="w-4 h-4 text-primary-gold rounded focus:ring-primary-gold"
          />
          <span class="text-sm font-medium text-gray-700">Make this donation anonymous</span>
        </label>
      </div>

      <!-- Terms -->
      <div>
        <label class="flex items-start space-x-2">
          <input
            v-model="formData.acceptTerms"
            type="checkbox"
            required
            class="w-4 h-4 text-primary-gold rounded focus:ring-primary-gold mt-1"
          />
          <span class="text-sm text-gray-600">
            I agree to the <a href="/terms" class="text-primary-gold hover:underline">Terms of Service</a> and 
            <a href="/privacy" class="text-primary-gold hover:underline">Privacy Policy</a>
          </span>
        </label>
      </div>

      <!-- Submit Button -->
      <Button
        type="submit"
        variant="primary"
        :disabled="processing || !isValid"
        class="w-full py-4 text-lg"
      >
        <span v-if="processing">
          <svg class="animate-spin -ml-1 mr-3 h-5 w-5 inline" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          Processing...
        </span>
        <span v-else>
          Donate {{ formattedAmount }}
        </span>
      </Button>

      <!-- Security Note -->
      <p class="text-center text-sm text-gray-500">
        🔒 Secure payment powered by Stripe
      </p>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { loadStripe, Stripe, StripeElements, StripeCardElement } from '@stripe/stripe-js'
import Button from '~/components/ui/Button.vue'

interface Props {
  publishableKey?: string
  campaigns?: Array<{ id: string; name: string }>
}

const props = withDefaults(defineProps<Props>(), {
  publishableKey: '',
  campaigns: () => []
})

const emit = defineEmits(['success', 'error'])

const loading = ref(true)
const processing = ref(false)
const error = ref('')
const stripe = ref<Stripe | null>(null)
const elements = ref<StripeElements | null>(null)
const cardElement = ref<StripeCardElement | null>(null)

const presetAmounts = [25, 50, 100, 250]
const frequencies = [
  { label: 'One-time', value: 'one_time' },
  { label: 'Monthly', value: 'monthly' },
  { label: 'Yearly', value: 'yearly' }
]

const selectedAmount = ref(50)
const customAmount = ref('')
const selectedFrequency = ref('one_time')

const formData = ref({
  firstName: '',
  lastName: '',
  email: '',
  phone: '',
  address: '',
  city: '',
  state: '',
  zip: '',
  isDedication: false,
  dedicationType: 'in_memory',
  dedicationName: '',
  dedicationEmail: '',
  campaignId: '',
  isAnonymous: false,
  acceptTerms: false
})

const formattedAmount = computed(() => {
  const amount = customAmount.value || selectedAmount.value
  return `$${amount}`
})

const isValid = computed(() => {
  const amount = customAmount.value || selectedAmount.value
  return (
    amount > 0 &&
    formData.value.firstName &&
    formData.value.lastName &&
    formData.value.email &&
    formData.value.acceptTerms
  )
})

const selectAmount = (amount: number) => {
  selectedAmount.value = amount
  customAmount.value = ''
}

const clearPreset = () => {
  if (customAmount.value) {
    selectedAmount.value = 0
  }
}

const selectFrequency = (frequency: string) => {
  selectedFrequency.value = frequency
}

const initializeStripe = async () => {
  try {
    if (!props.publishableKey) {
      throw new Error('Stripe publishable key is required')
    }

    stripe.value = await loadStripe(props.publishableKey)
    
    if (!stripe.value) {
      throw new Error('Failed to load Stripe')
    }

    elements.value = stripe.value.elements({
      appearance: {
        theme: 'stripe',
        variables: {
          colorPrimary: '#c9a84c',
          colorBackground: '#ffffff',
          colorText: '#1b2a4a',
        }
      }
    })

    cardElement.value = elements.value.create('card', {
      style: {
        base: {
          fontSize: '16px',
          color: '#1b2a4a',
          '::placeholder': {
            color: '#6b7280'
          }
        }
      }
    })

    cardElement.value.mount('#card-element')
    loading.value = false
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to initialize payment form'
    loading.value = false
  }
}

const handleSubmit = async () => {
  if (!stripe.value || !elements.value || !cardElement.value) {
    error.value = 'Payment system not initialized'
    return
  }

  processing.value = true
  error.value = ''

  try {
    const amount = customAmount.value || selectedAmount.value
    
    // Create payment intent on your backend
    const response = await fetch('/api/payments/create-payment-intent', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        amount: amount * 100, // Convert to cents
        currency: 'usd',
        frequency: selectedFrequency.value,
        donor: {
          firstName: formData.value.firstName,
          lastName: formData.value.lastName,
          email: formData.value.email,
          phone: formData.value.phone,
          address: formData.value.address,
          city: formData.value.city,
          state: formData.value.state,
          zip: formData.value.zip
        },
        dedication: formData.value.isDedication ? {
          type: formData.value.dedicationType,
          name: formData.value.dedicationName,
          email: formData.value.dedicationEmail
        } : null,
        campaignId: formData.value.campaignId || null,
        isAnonymous: formData.value.isAnonymous
      })
    })

    const { clientSecret, error: backendError } = await response.json()

    if (backendError) {
      throw new Error(backendError)
    }

    // Confirm payment with Stripe
    const { error: stripeError, paymentIntent } = await stripe.value.confirmCardPayment(clientSecret, {
      payment_method: {
        card: cardElement.value,
        billing_details: {
          name: `${formData.value.firstName} ${formData.value.lastName}`,
          email: formData.value.email,
          phone: formData.value.phone,
          address: {
            line1: formData.value.address,
            city: formData.value.city,
            state: formData.value.state,
            postal_code: formData.value.zip
          }
        }
      }
    })

    if (stripeError) {
      throw new Error(stripeError.message)
    }

    if (paymentIntent?.status === 'succeeded') {
      emit('success', { paymentIntent, formData: formData.value })
    }
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Payment failed'
    emit('error', error.value)
  } finally {
    processing.value = false
  }
}

onMounted(() => {
  initializeStripe()
})

onUnmounted(() => {
  if (cardElement.value) {
    cardElement.value.destroy()
  }
})
</script>
