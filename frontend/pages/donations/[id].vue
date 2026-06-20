<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <Button variant="ghost" @click="navigateTo('/donations')" class="mb-2">
          ← Back to Donations
        </Button>
        <h1 class="text-2xl font-display text-primary-navy">Donation Details</h1>
      </div>
      <div class="flex gap-2">
        <Button variant="secondary" @click="editMode = !editMode">
          {{ editMode ? 'Cancel' : 'Edit' }}
        </Button>
        <Button variant="danger" @click="deleteDonation">
          Delete
        </Button>
      </div>
    </div>

    <!-- Donation Details -->
    <Card hoverable>
      <template #header>
        <h3 class="text-lg font-display text-primary-navy">Donation Information</h3>
      </template>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label class="block text-sm font-medium text-gray-500 mb-1">Donor</label>
          <p class="text-lg font-medium text-primary-navy">{{ donation.donorName }}</p>
          <p class="text-sm text-gray-500">{{ donation.donorEmail }}</p>
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-500 mb-1">Amount</label>
          <p class="text-2xl font-display text-primary-emerald">${{ donation.amount.toLocaleString() }}</p>
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-500 mb-1">Type</label>
          <Badge :variant="donation.type === 'recurring' ? 'primary' : 'neutral'" size="sm">
            {{ donation.type === 'recurring' ? 'Recurring' : 'One-Time' }}
          </Badge>
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-500 mb-1">Status</label>
          <Badge :variant="getStatusVariant(donation.status)" size="sm">
            {{ donation.status }}
          </Badge>
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-500 mb-1">Campaign</label>
          <p class="text-lg font-medium text-primary-navy">{{ donation.campaign || 'General Fund' }}</p>
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-500 mb-1">Date</label>
          <p class="text-lg font-medium text-primary-navy">{{ donation.date }}</p>
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-500 mb-1">Payment Method</label>
          <p class="text-lg font-medium text-primary-navy">{{ donation.paymentMethod || 'Stripe' }}</p>
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-500 mb-1">Transaction ID</label>
          <p class="text-sm text-gray-600 font-mono">{{ donation.id }}</p>
        </div>
      </div>
      
      <div v-if="donation.notes" class="mt-6">
        <label class="block text-sm font-medium text-gray-500 mb-1">Notes</label>
        <p class="text-gray-700 bg-gray-50 p-3 rounded-lg">{{ donation.notes }}</p>
      </div>
    </Card>

    <!-- Edit Form -->
    <Card v-if="editMode" hoverable>
      <template #header>
        <h3 class="text-lg font-display text-primary-navy">Edit Donation</h3>
      </template>
      
      <form @submit.prevent="saveChanges" class="space-y-4">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium mb-2">Amount ($)</label>
            <input type="number" v-model="editForm.amount" class="input-field" required min="1" />
          </div>
          
          <div>
            <label class="block text-sm font-medium mb-2">Status</label>
            <select v-model="editForm.status" class="input-field">
              <option value="pending">Pending</option>
              <option value="completed">Completed</option>
              <option value="failed">Failed</option>
              <option value="refunded">Refunded</option>
            </select>
          </div>
          
          <div>
            <label class="block text-sm font-medium mb-2">Payment Method</label>
            <select v-model="editForm.paymentMethod" class="input-field">
              <option value="stripe">Stripe (Online)</option>
              <option value="check">Check</option>
              <option value="cash">Cash</option>
              <option value="transfer">Bank Transfer</option>
            </select>
          </div>
          
          <div>
            <label class="block text-sm font-medium mb-2">Campaign</label>
            <select v-model="editForm.campaignId" class="input-field">
              <option value="">General Fund</option>
              <option v-for="campaign in campaigns" :key="campaign.id" :value="campaign.id">
                {{ campaign.name }}
              </option>
            </select>
          </div>
        </div>
        
        <div>
          <label class="block text-sm font-medium mb-2">Notes</label>
          <textarea v-model="editForm.notes" class="input-field" rows="3"></textarea>
        </div>
        
        <div class="flex gap-2">
          <Button type="submit" variant="primary">Save Changes</Button>
          <Button type="button" variant="ghost" @click="editMode = false">Cancel</Button>
        </div>
      </form>
    </Card>

    <!-- Payment History -->
    <Card hoverable>
      <template #header>
        <h3 class="text-lg font-display text-primary-navy">Payment History</h3>
      </template>
      
      <div class="space-y-3">
        <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
          <div>
            <p class="font-medium text-primary-navy">{{ donation.paymentMethod || 'Stripe' }} Payment</p>
            <p class="text-sm text-gray-500">{{ donation.date }}</p>
          </div>
          <div class="text-right">
            <p class="font-medium text-primary-emerald">${{ donation.amount.toLocaleString() }}</p>
            <Badge :variant="getStatusVariant(donation.status)" size="sm">
              {{ donation.status }}
            </Badge>
          </div>
        </div>
      </div>
    </Card>
  </div>
</template>

<script setup lang="ts">
import Card from '~/components/ui/Card.vue'
import Button from '~/components/ui/Button.vue'
import Badge from '~/components/ui/Badge.vue'

const route = useRoute()
const editMode = ref(false)

const donation = ref({
  id: route.params.id,
  donorName: 'Ahmed Hassan',
  donorEmail: 'ahmed@example.com',
  amount: 500,
  type: 'one_time',
  campaign: 'Ramadan 2026',
  date: 'Mar 15, 2026',
  status: 'completed',
  paymentMethod: 'stripe',
  notes: 'Donation for Ramadan campaign'
})

const editForm = ref({
  amount: donation.value.amount,
  status: donation.value.status,
  paymentMethod: donation.value.paymentMethod,
  campaignId: '',
  notes: donation.value.notes
})

const campaigns = ref([
  { id: '1', name: 'Ramadan 2026' },
  { id: '2', name: 'Annual Fund' },
  { id: '3', name: 'Building Expansion' }
])

const getStatusVariant = (status: string) => {
  const variants: Record<string, string> = {
    completed: 'success',
    pending: 'warning',
    failed: 'danger',
    refunded: 'info'
  }
  return variants[status] || 'neutral'
}

const saveChanges = () => {
  donation.value.amount = editForm.value.amount
  donation.value.status = editForm.value.status
  donation.value.paymentMethod = editForm.value.paymentMethod
  donation.value.notes = editForm.value.notes
  
  const campaign = campaigns.value.find(c => c.id === editForm.value.campaignId)
  if (campaign) {
    donation.value.campaign = campaign.name
  }
  
  editMode.value = false
}

const deleteDonation = () => {
  if (confirm('Are you sure you want to delete this donation?')) {
    navigateTo('/donations')
  }
}
</script>
