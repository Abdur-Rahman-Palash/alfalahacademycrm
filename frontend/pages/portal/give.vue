<template>
  <div class="min-h-screen bg-primary-ivory">
    <!-- Header -->
    <header class="bg-primary-navy text-white py-8">
      <div class="max-w-4xl mx-auto px-4 text-center">
        <p class="text-sm font-arabic mb-2">بِسْمِ اللَّهِ</p>
        <h1 class="text-3xl font-display mb-2">Support Al Falah Academy</h1>
        <p class="text-white/80">Developing Muslim Youth in Academics and Character</p>
        <div class="mt-4 flex items-center justify-center gap-4 text-sm">
          <span>{{ gregorianDate }}</span>
          <span>|</span>
          <span class="font-arabic">{{ hijriDate }}</span>
        </div>
      </div>
    </header>

    <div class="max-w-4xl mx-auto px-4 py-8">
      <!-- Progress Steps -->
      <div class="flex items-center justify-center mb-8">
        <div class="flex items-center">
          <div 
            v-for="(step, index) in steps" 
            :key="step"
            class="flex items-center"
          >
            <div 
              class="w-10 h-10 rounded-full flex items-center justify-center font-medium"
              :class="currentStep >= index + 1 ? 'bg-primary-gold text-white' : 'bg-gray-200 text-gray-600'"
            >
              {{ index + 1 }}
            </div>
            <span 
              class="ml-2 text-sm font-medium"
              :class="currentStep >= index + 1 ? 'text-primary-navy' : 'text-gray-400'"
            >
              {{ step }}
            </span>
            <div 
              v-if="index < steps.length - 1" 
              class="w-16 h-1 mx-4"
              :class="currentStep > index + 1 ? 'bg-primary-gold' : 'bg-gray-200'"
            />
          </div>
        </div>
      </div>

      <!-- Step 1: Select Campaign -->
      <Card v-if="currentStep === 1" class="max-w-2xl mx-auto">
        <template #header>
          <h2 class="text-xl font-display text-primary-navy">Select a Campaign</h2>
        </template>
        
        <div class="space-y-4">
          <div 
            v-for="campaign in campaigns" 
            :key="campaign.id"
            @click="selectedCampaign = campaign.id"
            class="p-4 border-2 rounded-lg cursor-pointer transition-all"
            :class="selectedCampaign === campaign.id ? 'border-primary-gold bg-primary-gold/5' : 'border-gray-200 hover:border-primary-gold'"
          >
            <div class="flex items-start justify-between">
              <div>
                <h3 class="font-medium text-primary-navy">{{ campaign.name }}</h3>
                <p class="text-sm text-gray-500 mt-1">{{ campaign.description }}</p>
                <div class="mt-2">
                  <div class="flex items-center justify-between text-sm mb-1">
                    <span class="text-gray-600">${{ campaign.raised.toLocaleString() }} raised</span>
                    <span class="text-gray-600">${{ campaign.goal.toLocaleString() }} goal</span>
                  </div>
                  <div class="w-full bg-gray-200 rounded-full h-2">
                    <div 
                      class="bg-primary-gold h-2 rounded-full"
                      :style="{ width: campaign.progress + '%' }"
                    />
                  </div>
                </div>
              </div>
              <div v-if="selectedCampaign === campaign.id" class="w-6 h-6 rounded-full bg-primary-gold flex items-center justify-center text-white">
                ✓
              </div>
            </div>
          </div>
        </div>
        
        <div class="mt-6 flex justify-end">
          <Button variant="primary" :disabled="!selectedCampaign" @click="nextStep">
            Continue
          </Button>
        </div>
      </Card>

      <!-- Step 2: Choose Amount -->
      <Card v-if="currentStep === 2" class="max-w-2xl mx-auto">
        <template #header>
          <h2 class="text-xl font-display text-primary-navy">Choose Amount</h2>
        </template>
        
        <div class="space-y-6">
          <!-- Presets -->
          <div>
            <p class="text-sm font-medium text-gray-500 mb-3">Quick Select</p>
            <div class="grid grid-cols-4 gap-3">
              <button
                v-for="preset in donationPresets"
                :key="preset.amount"
                @click="selectedAmount = preset.amount"
                class="p-4 border-2 rounded-lg transition-all"
                :class="selectedAmount === preset.amount ? 'border-primary-gold bg-primary-gold/5' : 'border-gray-200 hover:border-primary-gold'"
              >
                <p class="text-2xl font-display text-primary-navy">${{ preset.amount }}</p>
                <p class="text-xs text-gray-500 mt-1">{{ preset.label }}</p>
              </button>
            </div>
          </div>
          
          <!-- Custom Amount -->
          <div>
            <p class="text-sm font-medium text-gray-500 mb-3">Or enter custom amount</p>
            <div class="relative">
              <span class="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500">$</span>
              <input
                v-model="customAmount"
                type="number"
                placeholder="Enter amount"
                class="input-field pl-8"
                @input="selectedAmount = null"
              />
            </div>
          </div>
          
          <!-- Frequency -->
          <div>
            <p class="text-sm font-medium text-gray-500 mb-3">Frequency</p>
            <div class="grid grid-cols-3 gap-3">
              <button
                v-for="freq in frequencies"
                :key="freq.value"
                @click="selectedFrequency = freq.value"
                class="p-3 border-2 rounded-lg transition-all text-center"
                :class="selectedFrequency === freq.value ? 'border-primary-gold bg-primary-gold/5' : 'border-gray-200 hover:border-primary-gold'"
              >
                <p class="font-medium">{{ freq.label }}</p>
              </button>
            </div>
          </div>
        </div>
        
        <div class="mt-6 flex justify-between">
          <Button variant="ghost" @click="prevStep">Back</Button>
          <Button variant="primary" :disabled="!finalAmount" @click="nextStep">
            Continue
          </Button>
        </div>
      </Card>

      <!-- Step 3: Donor Information -->
      <Card v-if="currentStep === 3" class="max-w-2xl mx-auto">
        <template #header>
          <h2 class="text-xl font-display text-primary-navy">Donor Information</h2>
        </template>
        
        <form @submit.prevent="nextStep" class="space-y-4">
          <div class="grid grid-cols-2 gap-4">
            <Input label="First Name" v-model="donorInfo.firstName" required />
            <Input label="Last Name" v-model="donorInfo.lastName" required />
          </div>
          
          <Input label="Email" type="email" v-model="donorInfo.email" required />
          <Input label="Phone" v-model="donorInfo.phone" />
          
          <div>
            <label class="flex items-center gap-2">
              <input type="checkbox" v-model="donorInfo.isAnonymous" />
              <span class="text-sm">Make this donation anonymous</span>
            </label>
          </div>
          
          <div>
            <label class="flex items-center gap-2">
              <input type="checkbox" v-model="donorInfo.receipt" />
              <span class="text-sm">Email me a tax receipt</span>
            </label>
          </div>
        </form>
        
        <div class="mt-6 flex justify-between">
          <Button variant="ghost" @click="prevStep">Back</Button>
          <Button variant="primary" @click="nextStep">
            Continue to Payment
          </Button>
        </div>
      </Card>

      <!-- Step 4: Payment -->
      <Card v-if="currentStep === 4" class="max-w-2xl mx-auto">
        <template #header>
          <h2 class="text-xl font-display text-primary-navy">Payment</h2>
        </template>
        
        <div class="space-y-6">
          <!-- Order Summary -->
          <div class="bg-primary-gray p-4 rounded-lg">
            <div class="flex justify-between mb-2">
              <span class="text-gray-600">Campaign</span>
              <span class="font-medium">{{ selectedCampaignName }}</span>
            </div>
            <div class="flex justify-between mb-2">
              <span class="text-gray-600">Amount</span>
              <span class="font-medium">${{ finalAmount }}</span>
            </div>
            <div class="flex justify-between mb-2">
              <span class="text-gray-600">Frequency</span>
              <span class="font-medium">{{ frequencyLabel }}</span>
            </div>
            <div class="border-t border-gray-300 pt-2 mt-2">
              <div class="flex justify-between">
                <span class="font-medium">Total</span>
                <span class="font-bold text-primary-navy">${{ finalAmount }}</span>
              </div>
            </div>
          </div>
          
          <!-- Stripe Elements Placeholder -->
          <div class="p-4 border border-gray-200 rounded-lg">
            <p class="text-sm text-gray-500 mb-4">Card Information</p>
            <div class="space-y-3">
              <input type="text" placeholder="Card number" class="input-field" />
              <div class="grid grid-cols-2 gap-3">
                <input type="text" placeholder="MM / YY" class="input-field" />
                <input type="text" placeholder="CVC" class="input-field" />
              </div>
            </div>
          </div>
          
          <p class="text-xs text-gray-500 text-center">
            🔒 Secure payment powered by Stripe
          </p>
        </div>
        
        <div class="mt-6 flex justify-between">
          <Button variant="ghost" @click="prevStep">Back</Button>
          <Button variant="primary" @click="handleDonate" :loading="isProcessing">
            {{ isProcessing ? 'Processing...' : `Donate $${finalAmount}` }}
          </Button>
        </div>
      </Card>

      <!-- Success -->
      <Card v-if="currentStep === 5" class="max-w-2xl mx-auto text-center">
        <div class="py-8">
          <div class="w-20 h-20 mx-auto mb-6 rounded-full bg-primary-emerald/10 flex items-center justify-center">
            <svg class="w-10 h-10 text-primary-emerald" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
          </div>
          
          <h2 class="text-2xl font-display text-primary-navy mb-2">JazakAllahu Khayran</h2>
          <p class="text-gray-600 mb-2">Thank you for your generous donation</p>
          <p class="text-gray-500 mb-6">May Allah reward you abundantly</p>
          
          <div class="bg-primary-gray p-4 rounded-lg text-left mb-6">
            <div class="flex justify-between mb-2">
              <span class="text-gray-600">Amount</span>
              <span class="font-medium">${{ finalAmount }}</span>
            </div>
            <div class="flex justify-between mb-2">
              <span class="text-gray-600">Campaign</span>
              <span class="font-medium">{{ selectedCampaignName }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">Confirmation #</span>
              <span class="font-medium">{{ confirmationNumber }}</span>
            </div>
          </div>
          
          <p class="text-sm text-gray-500 mb-4">A receipt has been sent to your email.</p>
          
          <div class="flex gap-3 justify-center">
            <Button variant="secondary" @click="printReceipt">
              Print Receipt
            </Button>
            <Button variant="primary" @click="resetForm">
              Make Another Donation
            </Button>
          </div>
        </div>
      </Card>
    </div>

    <!-- Footer -->
    <footer class="bg-primary-navy text-white py-8 mt-12">
      <div class="max-w-4xl mx-auto px-4 text-center">
        <p class="text-sm mb-2">Al Falah Academy</p>
        <p class="text-xs text-white/60">1835 Shackleford Ct, Norcross, GA 30093</p>
        <p class="text-xs text-white/60 mt-1">EIN: 27-2154656</p>
        <p class="text-xs text-white/40 mt-4">© 2026 Al Falah Academy. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import Card from '~/components/ui/Card.vue'
import Button from '~/components/ui/Button.vue'
import Input from '~/components/ui/Input.vue'
import { useHijriDate } from '~/composables/useHijriDate'
import { ISLAMIC_DONATION_PRESETS } from '~/utils/hijri'

const { dualDate } = useHijriDate()

const gregorianDate = computed(() => dualDate.value.gregorian)
const hijriDate = computed(() => dualDate.value.hijri)

const steps = ['Campaign', 'Amount', 'Info', 'Payment', 'Success']
const currentStep = ref(1)

const campaigns = ref([
  {
    id: '1',
    name: 'Ramadan 2026',
    description: 'Support our Ramadan programs and iftar meals',
    goal: 100000,
    raised: 85000,
    progress: 85
  },
  {
    id: '2',
    name: 'Annual Fund',
    description: 'General support for school operations and programs',
    goal: 75000,
    raised: 42500,
    progress: 57
  },
  {
    id: '3',
    name: 'Building Expansion',
    description: 'Help us grow and serve more students',
    goal: 500000,
    raised: 150000,
    progress: 30
  },
  {
    id: '4',
    name: 'GaSSO Scholarships',
    description: 'Support student scholarships through Georgia tax credits',
    goal: 250000,
    raised: 180000,
    progress: 72
  }
])

const donationPresets = ISLAMIC_DONATION_PRESETS

const frequencies = [
  { label: 'One-time', value: 'one_time' },
  { label: 'Monthly', value: 'monthly' },
  { label: 'Yearly', value: 'yearly' }
]

const selectedCampaign = ref('')
const selectedAmount = ref<number | null>(null)
const customAmount = ref('')
const selectedFrequency = ref('one_time')
const isProcessing = ref(false)

const donorInfo = ref({
  firstName: '',
  lastName: '',
  email: '',
  phone: '',
  isAnonymous: false,
  receipt: true
})

const finalAmount = computed(() => {
  if (selectedAmount.value) return selectedAmount.value
  if (customAmount.value) return parseFloat(customAmount.value) || 0
  return 0
})

const selectedCampaignName = computed(() => {
  const campaign = campaigns.value.find(c => c.id === selectedCampaign.value)
  return campaign?.name || ''
})

const frequencyLabel = computed(() => {
  const freq = frequencies.find(f => f.value === selectedFrequency.value)
  return freq?.label || ''
})

const confirmationNumber = ref('')

const nextStep = () => {
  if (currentStep.value < steps.length) {
    currentStep.value++
  }
}

const prevStep = () => {
  if (currentStep.value > 1) {
    currentStep.value--
  }
}

const handleDonate = async () => {
  isProcessing.value = true
  
  // Simulate payment processing
  await new Promise(resolve => setTimeout(resolve, 2000))
  
  // Generate confirmation number
  confirmationNumber.value = 'AFA-' + Date.now().toString(36).toUpperCase()
  
  isProcessing.value = false
  nextStep()
}

const printReceipt = () => {
  window.print()
}

const resetForm = () => {
  currentStep.value = 1
  selectedCampaign.value = ''
  selectedAmount.value = null
  customAmount.value = ''
  selectedFrequency.value = 'one_time'
  donorInfo.value = {
    firstName: '',
    lastName: '',
    email: '',
    phone: '',
    isAnonymous: false,
    receipt: true
  }
}
</script>
