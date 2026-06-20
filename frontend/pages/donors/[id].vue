<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-4">
        <Button variant="ghost" @click="navigateTo('/donors')">
          ← Back
        </Button>
        <div>
          <h1 class="text-2xl font-display text-primary-navy">{{ donor.name }}</h1>
          <p class="text-gray-500">{{ donor.email }}</p>
        </div>
      </div>
      <div class="flex gap-2">
        <Button variant="secondary" @click="editMode = !editMode">
          {{ editMode ? 'Cancel' : 'Edit' }}
        </Button>
        <Button variant="primary" @click="handleAddDonation">
          + Add Donation
        </Button>
      </div>
    </div>

    <!-- Donor Profile Card -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Profile Info -->
      <Card>
        <template #header>
          <h3 class="text-lg font-display text-primary-navy">Profile Information</h3>
        </template>
        
        <div v-if="!editMode" class="space-y-4">
          <div>
            <p class="text-sm text-gray-500">Name</p>
            <p class="font-medium">{{ donor.name }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-500">Organization</p>
            <p class="font-medium">{{ donor.orgName || 'N/A' }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-500">Email</p>
            <p class="font-medium">{{ donor.email }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-500">Phone</p>
            <p class="font-medium">{{ donor.phone || 'N/A' }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-500">Type</p>
            <Badge variant="neutral">{{ donor.type }}</Badge>
          </div>
          <div>
            <p class="text-sm text-gray-500 mb-2">Badges</p>
            <div class="flex gap-1 flex-wrap">
              <Badge v-if="donor.isDonor" variant="success">Donor</Badge>
              <Badge v-if="donor.isParent" variant="info">Parent</Badge>
              <Badge v-if="donor.isAlumni" variant="warning">Alumni</Badge>
              <Badge v-if="donor.isVolunteer" variant="neutral">Volunteer</Badge>
            </div>
          </div>
        </div>
        
        <form v-else @submit.prevent="handleSave" class="space-y-4">
          <div class="grid grid-cols-2 gap-4">
            <Input label="First Name" v-model="donor.firstName" />
            <Input label="Last Name" v-model="donor.lastName" />
          </div>
          <Input label="Organization" v-model="donor.orgName" />
          <Input label="Email" type="email" v-model="donor.email" />
          <Input label="Phone" v-model="donor.phone" />
          <div>
            <label class="block text-sm font-medium mb-2">Type</label>
            <select v-model="donor.type" class="input-field">
              <option value="individual">Individual</option>
              <option value="family">Family</option>
              <option value="corporate">Corporate</option>
              <option value="foundation">Foundation</option>
            </select>
          </div>
          <div class="flex gap-4">
            <label class="flex items-center gap-2">
              <input type="checkbox" v-model="donor.isDonor" />
              <span class="text-sm">Donor</span>
            </label>
            <label class="flex items-center gap-2">
              <input type="checkbox" v-model="donor.isParent" />
              <span class="text-sm">Parent</span>
            </label>
            <label class="flex items-center gap-2">
              <input type="checkbox" v-model="donor.isAlumni" />
              <span class="text-sm">Alumni</span>
            </label>
            <label class="flex items-center gap-2">
              <input type="checkbox" v-model="donor.isVolunteer" />
              <span class="text-sm">Volunteer</span>
            </label>
          </div>
          <Button type="submit" variant="primary" class="w-full">Save Changes</Button>
        </form>
      </Card>

      <!-- Giving Summary -->
      <Card>
        <template #header>
          <h3 class="text-lg font-display text-primary-navy">Giving Summary</h3>
        </template>
        
        <div class="space-y-4">
          <div class="text-center p-4 bg-primary-gray rounded-lg">
            <p class="text-3xl font-display text-primary-navy">${{ donor.lifetimeGiving.toLocaleString() }}</p>
            <p class="text-sm text-gray-500">Lifetime Total</p>
          </div>
          
          <div class="grid grid-cols-2 gap-4">
            <div class="text-center p-3 bg-primary-gray rounded-lg">
              <p class="text-xl font-display text-primary-navy">{{ donor.totalDonations }}</p>
              <p class="text-xs text-gray-500">Total Donations</p>
            </div>
            <div class="text-center p-3 bg-primary-gray rounded-lg">
              <p class="text-xl font-display text-primary-navy">${{ donor.avgDonation.toLocaleString() }}</p>
              <p class="text-xs text-gray-500">Average Gift</p>
            </div>
          </div>
          
          <div>
            <p class="text-sm text-gray-500 mb-2">Largest Gift</p>
            <p class="font-medium text-primary-emerald">${{ donor.largestGift.toLocaleString() }}</p>
          </div>
          
          <div>
            <p class="text-sm text-gray-500 mb-2">Last Donation</p>
            <p class="font-medium">{{ donor.lastDonationDate }}</p>
          </div>
        </div>
      </Card>

      <!-- Recurring Schedules -->
      <Card>
        <template #header>
          <h3 class="text-lg font-display text-primary-navy">Recurring Gifts</h3>
        </template>
        
        <div v-if="donor.recurringSchedules.length > 0" class="space-y-3">
          <div v-for="schedule in donor.recurringSchedules" :key="schedule.id" class="p-3 bg-primary-gray rounded-lg">
            <div class="flex items-center justify-between mb-2">
              <span class="font-medium">${{ schedule.amount.toLocaleString() }}</span>
              <Badge :variant="schedule.status === 'active' ? 'success' : 'neutral'" size="sm">
                {{ schedule.status }}
              </Badge>
            </div>
            <p class="text-sm text-gray-500">{{ schedule.frequency }}</p>
            <p class="text-xs text-gray-400">Next charge: {{ schedule.nextChargeDate }}</p>
          </div>
        </div>
        
        <div v-else class="text-center py-8 text-gray-500">
          <p>No recurring gifts</p>
          <Button variant="ghost" size="sm" class="mt-2">Set Up Recurring</Button>
        </div>
      </Card>
    </div>

    <!-- Donation History -->
    <Card>
      <template #header>
        <div class="flex items-center justify-between">
          <h3 class="text-lg font-display text-primary-navy">Donation History</h3>
          <Button variant="ghost" size="sm">Export</Button>
        </div>
      </template>
      
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead>
            <tr class="border-b border-gray-200">
              <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Date</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Amount</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Type</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Campaign</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Payment Method</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="donation in donor.donations" :key="donation.id" class="border-b border-gray-100 hover:bg-primary-gray/50">
              <td class="py-3 px-4 text-sm">
                {{ donation.date }}
                <span class="block text-xs text-gray-400">{{ donation.hijriDate }}</span>
              </td>
              <td class="py-3 px-4 text-sm font-medium text-primary-emerald">${{ donation.amount.toLocaleString() }}</td>
              <td class="py-3 px-4 text-sm">{{ donation.type }}</td>
              <td class="py-3 px-4 text-sm">{{ donation.campaign || 'N/A' }}</td>
              <td class="py-3 px-4 text-sm">{{ donation.paymentMethod }}</td>
              <td class="py-3 px-4">
                <Badge :variant="donation.status === 'completed' ? 'success' : 'warning'" size="sm">
                  {{ donation.status }}
                </Badge>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </Card>

    <!-- Add Donation Modal -->
    <Modal v-if="showDonationModal" @close="showDonationModal = false">
      <template #header>
        <h2 class="text-xl font-display text-primary-navy">Add Donation</h2>
      </template>
      
      <form @submit.prevent="handleSaveDonation" class="space-y-4">
        <div>
          <label class="block text-sm font-medium mb-2">Amount</label>
          <input type="number" v-model="newDonation.amount" class="input-field" required />
        </div>
        
        <div>
          <label class="block text-sm font-medium mb-2">Type</label>
          <select v-model="newDonation.type" class="input-field">
            <option value="one_time">One-time</option>
            <option value="recurring">Recurring</option>
            <option value="pledge">Pledge</option>
            <option value="in_kind">In-kind</option>
          </select>
        </div>
        
        <div>
          <label class="block text-sm font-medium mb-2">Campaign</label>
          <select v-model="newDonation.campaignId" class="input-field">
            <option value="">No Campaign</option>
            <option value="1">Ramadan 2026</option>
            <option value="2">Annual Fund</option>
            <option value="3">Building Expansion</option>
          </select>
        </div>
        
        <div>
          <label class="block text-sm font-medium mb-2">Payment Method</label>
          <select v-model="newDonation.paymentMethod" class="input-field">
            <option value="stripe">Stripe</option>
            <option value="check">Check</option>
            <option value="cash">Cash</option>
            <option value="zelle">Zelle</option>
          </select>
        </div>
      </form>
      
      <template #footer>
        <Button variant="ghost" @click="showDonationModal = false">Cancel</Button>
        <Button variant="primary" @click="handleSaveDonation">Save Donation</Button>
      </template>
    </Modal>
  </div>
</template>

<script setup lang="ts">
import Card from '~/components/ui/Card.vue'
import Button from '~/components/ui/Button.vue'
import Input from '~/components/ui/Input.vue'
import Badge from '~/components/ui/Badge.vue'
import Modal from '~/components/ui/Modal.vue'

const route = useRoute()
const editMode = ref(false)
const showDonationModal = ref(false)

// Mock donor data - replace with API call
const donor = ref({
  id: '1',
  name: 'Ahmed Family',
  firstName: 'Ahmed',
  lastName: 'Family',
  orgName: '',
  email: 'ahmed.family@example.com',
  phone: '(555) 123-4567',
  type: 'family',
  lifetimeGiving: 15000,
  totalDonations: 12,
  avgDonation: 1250,
  largestGift: 5000,
  lastDonationDate: 'June 15, 2026',
  isDonor: true,
  isParent: true,
  isAlumni: false,
  isVolunteer: false,
  recurringSchedules: [
    {
      id: '1',
      amount: 100,
      frequency: 'monthly',
      status: 'active',
      nextChargeDate: 'July 1, 2026'
    }
  ],
  donations: [
    {
      id: '1',
      date: 'June 15, 2026',
      hijriDate: '23 Dhul Hijjah 1447',
      amount: 500,
      type: 'one_time',
      campaign: 'Ramadan 2026',
      paymentMethod: 'stripe',
      status: 'completed'
    },
    {
      id: '2',
      date: 'May 20, 2026',
      hijriDate: '12 Shawwal 1447',
      amount: 1000,
      type: 'one_time',
      campaign: 'Annual Fund',
      paymentMethod: 'check',
      status: 'completed'
    }
  ]
})

const newDonation = ref({
  amount: 0,
  type: 'one_time',
  campaignId: '',
  paymentMethod: 'stripe'
})

const handleAddDonation = () => {
  showDonationModal.value = true
}

const handleSaveDonation = () => {
  // TODO: Implement save logic
  console.log('Saving donation:', newDonation.value)
  showDonationModal.value = false
}

const handleSave = () => {
  // TODO: Implement save logic
  console.log('Saving donor:', donor.value)
  editMode.value = false
}
</script>
