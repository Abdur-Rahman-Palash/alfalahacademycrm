<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-display text-primary-navy">Donations</h1>
        <p class="text-gray-500">Manage donations and payment records</p>
      </div>
      <Button variant="primary" @click="showAddModal = true">
        + Add Donation
      </Button>
    </div>

    <!-- Donation Stats -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
      <Card class="scale-in hover-lift" style="animation-delay: 0.1s">
        <div class="text-center">
          <p class="text-3xl font-display text-primary-navy">{{ totalDonations }}</p>
          <p class="text-sm text-gray-500">Total Donations</p>
        </div>
      </Card>
      <Card class="scale-in hover-lift" style="animation-delay: 0.2s">
        <div class="text-center">
          <p class="text-3xl font-display text-primary-emerald">${{ totalAmount.toLocaleString() }}</p>
          <p class="text-sm text-gray-500">Total Amount</p>
        </div>
      </Card>
      <Card class="scale-in hover-lift" style="animation-delay: 0.3s">
        <div class="text-center">
          <p class="text-3xl font-display text-primary-gold">{{ recurringCount }}</p>
          <p class="text-sm text-gray-500">Recurring</p>
        </div>
      </Card>
      <Card class="scale-in hover-lift" style="animation-delay: 0.4s">
        <div class="text-center">
          <p class="text-3xl font-display text-primary-navy">{{ thisMonthCount }}</p>
          <p class="text-sm text-gray-500">This Month</p>
        </div>
      </Card>
    </div>

    <!-- Donations List -->
    <Card class="fade-in-up" style="animation-delay: 0.5s" hoverable>
      <template #header>
        <div class="flex items-center justify-between">
          <h3 class="text-lg font-display text-primary-navy">All Donations</h3>
          <div class="flex gap-2">
            <select v-model="filterStatus" class="input-field w-40">
              <option value="">All Status</option>
              <option value="completed">Completed</option>
              <option value="pending">Pending</option>
              <option value="failed">Failed</option>
            </select>
            <select v-model="filterType" class="input-field w-40">
              <option value="">All Types</option>
              <option value="one_time">One-Time</option>
              <option value="recurring">Recurring</option>
            </select>
          </div>
        </div>
      </template>
      
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead>
            <tr class="border-b border-gray-200">
              <th class="text-left py-3 px-4 text-sm font-medium text-gray-600">Donor</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-gray-600">Amount</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-gray-600">Type</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-gray-600">Campaign</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-gray-600">Date</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-gray-600">Status</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-gray-600">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="donation in filteredDonations" :key="donation.id" class="border-b border-gray-100 hover:bg-gray-50">
              <td class="py-3 px-4">
                <div>
                  <p class="font-medium text-primary-navy">{{ donation.donorName }}</p>
                  <p class="text-xs text-gray-500">{{ donation.donorEmail }}</p>
                </div>
              </td>
              <td class="py-3 px-4 text-sm font-medium">${{ donation.amount.toLocaleString() }}</td>
              <td class="py-3 px-4 text-sm">
                <Badge :variant="donation.type === 'recurring' ? 'primary' : 'neutral'" size="sm">
                  {{ donation.type === 'recurring' ? 'Recurring' : 'One-Time' }}
                </Badge>
              </td>
              <td class="py-3 px-4 text-sm">{{ donation.campaign || 'General' }}</td>
              <td class="py-3 px-4 text-sm">{{ donation.date }}</td>
              <td class="py-3 px-4">
                <Badge :variant="getStatusVariant(donation.status)" size="sm">
                  {{ donation.status }}
                </Badge>
              </td>
              <td class="py-3 px-4">
                <div class="flex gap-2">
                  <Button variant="ghost" size="sm" @click="viewDetails(donation.id)">
                    View
                  </Button>
                  <Button variant="ghost" size="sm" @click="editDonation(donation.id)">
                    Edit
                  </Button>
                  <Button variant="ghost" size="sm" @click="deleteDonation(donation.id)">
                    Delete
                  </Button>
                  <Button v-if="donation.status === 'pending'" variant="secondary" size="sm" @click="processPayment(donation.id)">
                    Process
                  </Button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </Card>

    <!-- Add Donation Modal -->
    <Modal :isOpen="showAddModal" @close="showAddModal = false">
      <template #header>
        <h2 class="text-xl font-display text-primary-navy">Add New Donation</h2>
      </template>
      
      <form id="addDonationForm" @submit.prevent="handleAdd" class="space-y-4">
        <div>
          <label class="block text-sm font-medium mb-2">Donor</label>
          <select v-model="newDonation.donorId" class="input-field" required>
            <option value="">Select a donor</option>
            <option v-for="donor in donors" :key="donor.id" :value="donor.id">
              {{ donor.name }}
            </option>
          </select>
        </div>
        
        <div>
          <label class="block text-sm font-medium mb-2">Amount ($)</label>
          <input type="number" v-model="newDonation.amount" class="input-field" required min="1" />
        </div>
        
        <div>
          <label class="block text-sm font-medium mb-2">Donation Type</label>
          <select v-model="newDonation.type" class="input-field">
            <option value="one_time">One-Time</option>
            <option value="recurring">Recurring</option>
          </select>
        </div>
        
        <div v-if="newDonation.type === 'recurring'">
          <label class="block text-sm font-medium mb-2">Frequency</label>
          <select v-model="newDonation.frequency" class="input-field">
            <option value="monthly">Monthly</option>
            <option value="yearly">Yearly</option>
          </select>
        </div>
        
        <div>
          <label class="block text-sm font-medium mb-2">Campaign</label>
          <select v-model="newDonation.campaignId" class="input-field">
            <option value="">General Fund</option>
            <option v-for="campaign in campaigns" :key="campaign.id" :value="campaign.id">
              {{ campaign.name }}
            </option>
          </select>
        </div>
        
        <div>
          <label class="block text-sm font-medium mb-2">Payment Method</label>
          <select v-model="newDonation.paymentMethod" class="input-field">
            <option value="stripe">Stripe (Online)</option>
            <option value="check">Check</option>
            <option value="cash">Cash</option>
            <option value="transfer">Bank Transfer</option>
          </select>
        </div>
        
        <div>
          <label class="block text-sm font-medium mb-2">Notes</label>
          <textarea v-model="newDonation.notes" class="input-field" rows="3"></textarea>
        </div>
        
        <div class="flex gap-2">
          <Button type="button" variant="ghost" @click="showAddModal = false">Cancel</Button>
          <Button type="submit" variant="primary">Add Donation</Button>
        </div>
      </form>
    </Modal>

    <!-- Edit Donation Modal -->
    <Modal :isOpen="showEditModal" @close="showEditModal = false">
      <template #header>
        <h2 class="text-xl font-display text-primary-navy">Edit Donation</h2>
      </template>
      
      <form @submit.prevent="handleEdit" class="space-y-4">
        <div>
          <label class="block text-sm font-medium mb-2">Amount ($)</label>
          <input type="number" v-model="editingDonation.amount" class="input-field" required min="1" />
        </div>
        
        <div>
          <label class="block text-sm font-medium mb-2">Status</label>
          <select v-model="editingDonation.status" class="input-field">
            <option value="pending">Pending</option>
            <option value="completed">Completed</option>
            <option value="failed">Failed</option>
          </select>
        </div>
        
        <div>
          <label class="block text-sm font-medium mb-2">Notes</label>
          <textarea v-model="editingDonation.notes" class="input-field" rows="3"></textarea>
        </div>
        
        <div class="flex gap-2">
          <Button type="button" variant="ghost" @click="showEditModal = false">Cancel</Button>
          <Button type="submit" variant="primary">Save Changes</Button>
        </div>
      </form>
    </Modal>
  </div>
</template>

<script setup lang="ts">
import Card from '~/components/ui/Card.vue'
import Button from '~/components/ui/Button.vue'
import Badge from '~/components/ui/Badge.vue'
import Modal from '~/components/ui/Modal.vue'

const filterStatus = ref('')
const filterType = ref('')
const showAddModal = ref(false)
const showEditModal = ref(false)
const editingDonation = ref<any>(null)

const newDonation = ref({
  donorId: '',
  amount: 0,
  type: 'one_time',
  frequency: 'monthly',
  campaignId: '',
  paymentMethod: 'stripe',
  notes: ''
})

// Mock data
const donations = ref([
  {
    id: '1',
    donorName: 'Ahmed Hassan',
    donorEmail: 'ahmed@example.com',
    amount: 500,
    type: 'one_time',
    campaign: 'Ramadan 2026',
    date: 'Mar 15, 2026',
    status: 'completed'
  },
  {
    id: '2',
    donorName: 'Fatima Ahmed',
    donorEmail: 'fatima@example.com',
    amount: 100,
    type: 'recurring',
    campaign: 'Annual Fund',
    date: 'Mar 14, 2026',
    status: 'completed'
  },
  {
    id: '3',
    donorName: 'Omar Khalid',
    donorEmail: 'omar@example.com',
    amount: 250,
    type: 'one_time',
    campaign: 'Building Expansion',
    date: 'Mar 13, 2026',
    status: 'pending'
  },
  {
    id: '4',
    donorName: 'Aisha Mohammed',
    donorEmail: 'aisha@example.com',
    amount: 1000,
    type: 'one_time',
    campaign: 'General',
    date: 'Mar 12, 2026',
    status: 'completed'
  }
])

const donors = ref([
  { id: '1', name: 'Ahmed Hassan', email: 'ahmed@example.com' },
  { id: '2', name: 'Fatima Ahmed', email: 'fatima@example.com' },
  { id: '3', name: 'Omar Khalid', email: 'omar@example.com' },
  { id: '4', name: 'Aisha Mohammed', email: 'aisha@example.com' }
])

const campaigns = ref([
  { id: '1', name: 'Ramadan 2026' },
  { id: '2', name: 'Annual Fund' },
  { id: '3', name: 'Building Expansion' }
])

const filteredDonations = computed(() => {
  return donations.value.filter(donation => {
    const matchesStatus = !filterStatus.value || donation.status === filterStatus.value
    const matchesType = !filterType.value || donation.type === filterType.value
    return matchesStatus && matchesType
  })
})

const totalDonations = computed(() => donations.value.length)
const totalAmount = computed(() => donations.value.reduce((sum, d) => sum + d.amount, 0))
const recurringCount = computed(() => donations.value.filter(d => d.type === 'recurring').length)
const thisMonthCount = computed(() => donations.value.filter(d => d.date.includes('Mar')).length)

const getStatusVariant = (status: string) => {
  const variants: Record<string, string> = {
    completed: 'success',
    pending: 'warning',
    failed: 'danger',
    refunded: 'info'
  }
  return variants[status] || 'neutral'
}

const viewDetails = (id: string) => {
  navigateTo(`/donations/${id}`)
}

const processPayment = (id: string) => {
  const donation = donations.value.find(d => d.id === id)
  if (donation) {
    donation.status = 'completed'
  }
}

const editDonation = (id: string) => {
  const donation = donations.value.find(d => d.id === id)
  if (donation) {
    editingDonation.value = { ...donation }
    showEditModal.value = true
  }
}

const handleEdit = () => {
  const index = donations.value.findIndex(d => d.id === editingDonation.value.id)
  if (index !== -1) {
    donations.value[index] = { ...editingDonation.value }
    showEditModal.value = false
    editingDonation.value = null
  }
}

const deleteDonation = (id: string) => {
  if (confirm('Are you sure you want to delete this donation?')) {
    donations.value = donations.value.filter(d => d.id !== id)
  }
}

const handleAdd = () => {
  const donor = donors.value.find(d => d.id === newDonation.value.donorId)
  const campaign = campaigns.value.find(c => c.id === newDonation.value.campaignId)
  
  const donation = {
    id: Date.now().toString(),
    donorName: donor?.name || 'Unknown',
    donorEmail: donor?.email || '',
    amount: newDonation.value.amount,
    type: newDonation.value.type,
    campaign: campaign?.name || 'General',
    date: new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }),
    status: 'pending'
  }
  
  donations.value.unshift(donation)
  showAddModal.value = false
  
  // Reset form
  newDonation.value = {
    donorId: '',
    amount: 0,
    type: 'one_time',
    frequency: 'monthly',
    campaignId: '',
    paymentMethod: 'stripe',
    notes: ''
  }
}
</script>
