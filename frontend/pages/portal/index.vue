<template>
  <div class="min-h-screen bg-primary-ivory">
    <!-- Portal Header -->
    <div class="gradient-bg text-white py-8 px-4">
      <div class="max-w-6xl mx-auto">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-3xl font-display font-bold mb-2">Donor Portal</h1>
            <p class="text-white/80">Welcome back, {{ donorName }}</p>
          </div>
          <Button variant="secondary" @click="showDonateModal = true">
            Make a Donation
          </Button>
        </div>
      </div>
    </div>

    <div class="max-w-6xl mx-auto px-4 py-8 space-y-8">
      <!-- Impact Summary -->
      <Card class="scale-in hover-lift" style="animation-delay: 0.1s">
        <template #header>
          <h3 class="text-lg font-display text-primary-navy">Your Impact</h3>
        </template>
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div class="text-center">
            <p class="text-4xl font-display text-primary-gold">${{ totalDonated.toLocaleString() }}</p>
            <p class="text-sm text-gray-500 mt-1">Total Donated</p>
          </div>
          <div class="text-center">
            <p class="text-4xl font-display text-primary-emerald">{{ donationCount }}</p>
            <p class="text-sm text-gray-500 mt-1">Donations Made</p>
          </div>
          <div class="text-center">
            <p class="text-4xl font-display text-primary-navy">{{ campaignsSupported }}</p>
            <p class="text-sm text-gray-500 mt-1">Campaigns Supported</p>
          </div>
          <div class="text-center">
            <p class="text-4xl font-display text-primary-navy">{{ yearsActive }}</p>
            <p class="text-sm text-gray-500 mt-1">Years Active</p>
          </div>
        </div>
      </Card>

      <!-- Quick Actions -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card class="fade-in-up hover-lift cursor-pointer" style="animation-delay: 0.2s" @click="showDonateModal = true">
          <div class="text-center">
            <div class="w-16 h-16 bg-primary-gold/20 rounded-full flex items-center justify-center mx-auto mb-3">
              <span class="text-3xl">💰</span>
            </div>
            <h4 class="font-semibold text-primary-navy mb-1">Make a Donation</h4>
            <p class="text-sm text-gray-500">Support our mission</p>
          </div>
        </Card>
        
        <Card class="fade-in-up hover-lift cursor-pointer" style="animation-delay: 0.3s" @click="showRecurringModal = true">
          <div class="text-center">
            <div class="w-16 h-16 bg-primary-emerald/20 rounded-full flex items-center justify-center mx-auto mb-3">
              <span class="text-3xl">🔄</span>
            </div>
            <h4 class="font-semibold text-primary-navy mb-1">Recurring Giving</h4>
            <p class="text-sm text-gray-500">Set up monthly donations</p>
          </div>
        </Card>
        
        <Card class="fade-in-up hover-lift cursor-pointer" style="animation-delay: 0.4s" @click="showHistoryModal = true">
          <div class="text-center">
            <div class="w-16 h-16 bg-primary-navy/20 rounded-full flex items-center justify-center mx-auto mb-3">
              <span class="text-3xl">📊</span>
            </div>
            <h4 class="font-semibold text-primary-navy mb-1">Donation History</h4>
            <p class="text-sm text-gray-500">View your giving history</p>
          </div>
        </Card>
      </div>

      <!-- Recent Donations -->
      <Card class="fade-in-up" style="animation-delay: 0.5s" hoverable>
        <template #header>
          <div class="flex items-center justify-between">
            <h3 class="text-lg font-display text-primary-navy">Recent Donations</h3>
            <Button variant="ghost" size="sm" @click="showHistoryModal = true">
              View All
            </Button>
          </div>
        </template>
        <div class="space-y-4">
          <div v-for="donation in recentDonations" :key="donation.id" class="flex items-center justify-between p-4 bg-primary-gray rounded-lg">
            <div class="flex items-center gap-4">
              <div class="w-12 h-12 bg-primary-gold/20 rounded-full flex items-center justify-center">
                <span class="text-2xl">💵</span>
              </div>
              <div>
                <p class="font-medium text-primary-navy">${{ donation.amount.toLocaleString() }}</p>
                <p class="text-sm text-gray-500">{{ donation.campaign || 'General Donation' }}</p>
              </div>
            </div>
            <div class="text-right">
              <p class="text-sm text-gray-600">{{ donation.date }}</p>
              <Badge :variant="donation.status === 'completed' ? 'success' : 'warning'" size="sm">
                {{ donation.status }}
              </Badge>
            </div>
          </div>
        </div>
      </Card>

      <!-- Active Recurring Donations -->
      <Card v-if="recurringDonations.length > 0" class="fade-in-up" style="animation-delay: 0.6s" hoverable>
        <template #header>
          <h3 class="text-lg font-display text-primary-navy">Active Recurring Donations</h3>
        </template>
        <div class="space-y-4">
          <div v-for="recurring in recurringDonations" :key="recurring.id" class="p-4 border border-gray-200 rounded-lg">
            <div class="flex items-center justify-between mb-3">
              <div>
                <p class="font-semibold text-primary-navy">${{ recurring.amount.toLocaleString() }} / {{ recurring.frequency }}</p>
                <p class="text-sm text-gray-500">{{ recurring.campaign || 'General Fund' }}</p>
              </div>
              <Badge variant="success" size="sm">Active</Badge>
            </div>
            <div class="flex items-center justify-between text-sm">
              <span class="text-gray-600">Next payment: {{ recurring.nextPayment }}</span>
              <Button variant="ghost" size="sm" @click="manageRecurring(recurring.id)">
                Manage
              </Button>
            </div>
          </div>
        </div>
      </Card>

      <!-- Campaign Impact -->
      <Card class="fade-in-up" style="animation-delay: 0.7s" hoverable>
        <template #header>
          <h3 class="text-lg font-display text-primary-navy">Campaigns You've Supported</h3>
        </template>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div v-for="campaign in supportedCampaigns" :key="campaign.id" class="p-4 border border-gray-200 rounded-lg hover:border-primary-gold transition-colors">
            <div class="flex items-start justify-between mb-3">
              <div>
                <h4 class="font-medium text-primary-navy">{{ campaign.name }}</h4>
                <p class="text-sm text-gray-500">{{ campaign.type }}</p>
              </div>
              <Badge variant="success" size="sm">{{ campaign.status }}</Badge>
            </div>
            <div class="space-y-2">
              <div class="flex justify-between text-sm">
                <span class="text-gray-600">Your contribution</span>
                <span class="font-medium">${{ campaign.yourContribution.toLocaleString() }}</span>
              </div>
              <div class="w-full bg-gray-200 rounded-full h-2">
                <div 
                  class="bg-primary-gold h-2 rounded-full"
                  :style="{ width: campaign.progress + '%' }"
                />
              </div>
              <div class="flex justify-between text-xs text-gray-500">
                <span>{{ campaign.progress }}% funded</span>
                <span>${{ campaign.raised.toLocaleString() }} raised</span>
              </div>
            </div>
          </div>
        </div>
      </Card>

      <!-- Account Settings -->
      <Card class="fade-in-up" style="animation-delay: 0.8s" hoverable>
        <template #header>
          <h3 class="text-lg font-display text-primary-navy">Account Settings</h3>
        </template>
        <div class="space-y-4">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium mb-2">Email Address</label>
              <input type="email" v-model="donorInfo.email" class="input-field" />
            </div>
            <div>
              <label class="block text-sm font-medium mb-2">Phone Number</label>
              <input type="tel" v-model="donorInfo.phone" class="input-field" />
            </div>
            <div>
              <label class="block text-sm font-medium mb-2">Address</label>
              <input type="text" v-model="donorInfo.address" class="input-field" />
            </div>
            <div>
              <label class="block text-sm font-medium mb-2">City</label>
              <input type="text" v-model="donorInfo.city" class="input-field" />
            </div>
          </div>
          <div class="flex gap-2">
            <Button variant="primary" @click="saveSettings">
              Save Changes
            </Button>
            <Button variant="ghost" @click="downloadTaxReceipts">
              Download Tax Receipts
            </Button>
          </div>
        </div>
      </Card>
    </div>

    <!-- Quick Donate Modal -->
    <Modal v-if="showDonateModal" @close="showDonateModal = false">
      <template #header>
        <h2 class="text-xl font-display text-primary-navy">Make a Donation</h2>
      </template>
      <StripePaymentForm
        :publishableKey="stripePublishableKey"
        :campaigns="availableCampaigns"
        @success="handleDonationSuccess"
        @error="handleDonationError"
      />
    </Modal>

    <!-- Recurring Donation Modal -->
    <Modal v-if="showRecurringModal" @close="showRecurringModal = false">
      <template #header>
        <h2 class="text-xl font-display text-primary-navy">Set Up Recurring Donation</h2>
      </template>
      <div class="space-y-4">
        <div>
          <label class="block text-sm font-medium mb-2">Monthly Amount</label>
          <div class="grid grid-cols-4 gap-2 mb-3">
            <button
              v-for="amount in [25, 50, 100, 250]"
              :key="amount"
              @click="recurringAmount = amount"
              :class="[
                'py-3 px-4 rounded-lg border-2 transition-all',
                recurringAmount === amount
                  ? 'border-primary-gold bg-primary-gold text-white'
                  : 'border-gray-200 hover:border-primary-gold'
              ]"
            >
              ${{ amount }}
            </button>
          </div>
          <input
            v-model="customRecurringAmount"
            type="number"
            placeholder="Custom amount"
            class="input-field"
          />
        </div>
        <div>
          <label class="block text-sm font-medium mb-2">Apply to Campaign</label>
          <select v-model="recurringCampaign" class="input-field">
            <option value="">General Fund</option>
            <option v-for="campaign in availableCampaigns" :key="campaign.id" :value="campaign.id">
              {{ campaign.name }}
            </option>
          </select>
        </div>
        <Button variant="primary" class="w-full" @click="setupRecurring">
          Set Up Monthly Donation
        </Button>
      </div>
    </Modal>

    <!-- Donation History Modal -->
    <Modal v-if="showHistoryModal" @close="showHistoryModal = false" size="large">
      <template #header>
        <h2 class="text-xl font-display text-primary-navy">Donation History</h2>
      </template>
      <div class="space-y-4">
        <div v-for="donation in allDonations" :key="donation.id" class="p-4 border border-gray-200 rounded-lg">
          <div class="flex items-center justify-between">
            <div>
              <p class="font-semibold text-primary-navy">${{ donation.amount.toLocaleString() }}</p>
              <p class="text-sm text-gray-500">{{ donation.campaign || 'General Donation' }}</p>
              <p class="text-xs text-gray-400">{{ donation.date }}</p>
            </div>
            <div class="text-right">
              <Badge :variant="donation.status === 'completed' ? 'success' : 'warning'" size="sm">
                {{ donation.status }}
              </Badge>
              <Button variant="ghost" size="sm" class="mt-2" @click="downloadReceipt(donation.id)">
                Receipt
              </Button>
            </div>
          </div>
        </div>
      </div>
    </Modal>
  </div>
</template>

<script setup lang="ts">
import Card from '~/components/ui/Card.vue'
import Button from '~/components/ui/Button.vue'
import Badge from '~/components/ui/Badge.vue'
import Modal from '~/components/ui/Modal.vue'
import StripePaymentForm from '~/components/stripe/StripePaymentForm.vue'

const donorName = ref('Ahmed Hassan')
const stripePublishableKey = ref('pk_test_placeholder')

const donorInfo = ref({
  email: 'ahmed.hassan@example.com',
  phone: '(555) 123-4567',
  address: '123 Main Street',
  city: 'Atlanta'
})

const showDonateModal = ref(false)
const showRecurringModal = ref(false)
const showHistoryModal = ref(false)

const recurringAmount = ref(50)
const customRecurringAmount = ref('')
const recurringCampaign = ref('')

// Mock data
const recentDonations = ref([
  { id: '1', amount: 500, campaign: 'Ramadan 2026', date: 'Mar 15, 2026', status: 'completed' },
  { id: '2', amount: 250, campaign: 'Annual Fund', date: 'Feb 28, 2026', status: 'completed' },
  { id: '3', amount: 1000, campaign: 'Building Expansion', date: 'Jan 10, 2026', status: 'completed' }
])

const recurringDonations = ref([
  { id: '1', amount: 100, frequency: 'month', campaign: 'Annual Fund', nextPayment: 'Apr 15, 2026' }
])

const supportedCampaigns = ref([
  { id: '1', name: 'Ramadan 2026', type: 'Ramadan', status: 'Active', yourContribution: 500, progress: 85, raised: 85000 },
  { id: '2', name: 'Annual Fund 2026', type: 'Annual', status: 'Active', yourContribution: 250, progress: 57, raised: 42500 }
])

const availableCampaigns = ref([
  { id: '1', name: 'Ramadan 2026' },
  { id: '2', name: 'Annual Fund 2026' },
  { id: '3', name: 'Building Expansion' }
])

const allDonations = ref([
  ...recentDonations.value,
  { id: '4', amount: 750, campaign: 'Dhul Hijjah 2025', date: 'Jun 20, 2025', status: 'completed' },
  { id: '5', amount: 150, campaign: 'General Fund', date: 'May 15, 2025', status: 'completed' }
])

const totalDonated = computed(() => allDonations.value.reduce((sum, d) => sum + d.amount, 0))
const donationCount = computed(() => allDonations.value.length)
const campaignsSupported = computed(() => supportedCampaigns.value.length)
const yearsActive = computed(() => 2)

const handleDonationSuccess = (data: any) => {
  console.log('Donation successful:', data)
  showDonateModal.value = false
  // Refresh donation data
}

const handleDonationError = (error: string) => {
  console.error('Donation error:', error)
}

const setupRecurring = () => {
  const amount = customRecurringAmount.value || recurringAmount.value
  console.log('Setting up recurring donation:', amount, recurringCampaign.value)
  showRecurringModal.value = false
}

const manageRecurring = (id: string) => {
  console.log('Manage recurring:', id)
}

const saveSettings = () => {
  console.log('Saving settings:', donorInfo.value)
}

const downloadTaxReceipts = () => {
  console.log('Downloading tax receipts')
}

const downloadReceipt = (id: string) => {
  console.log('Downloading receipt for:', id)
}
</script>
