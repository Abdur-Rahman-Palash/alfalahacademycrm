<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-display text-primary-navy">Campaigns</h1>
        <p class="text-gray-500">Manage fundraising campaigns and Islamic giving initiatives</p>
      </div>
      <Button variant="primary" @click="showCreateModal = true">
        + Create Campaign
      </Button>
    </div>

    <!-- Islamic Calendar Widget -->
    <Card class="bg-gradient-to-r from-primary-navy to-primary-gold text-white">
      <div class="flex items-center justify-between">
        <div>
          <h3 class="text-xl font-display mb-2">Islamic Calendar</h3>
          <p class="text-sm opacity-90">Current Hijri Date: {{ currentHijriDate }}</p>
          <p class="text-sm opacity-90 mt-1" v-if="isRamadan">🌙 Ramadan - Special giving period</p>
          <p class="text-sm opacity-90 mt-1" v-else-if="isDhulHijjah">🌙 Dhul Hijjah - Special giving period</p>
        </div>
        <div class="text-right">
          <p class="text-4xl font-arabic">☪</p>
          <p class="text-sm mt-2 opacity-75">بِسْمِ اللَّهِ</p>
        </div>
      </div>
    </Card>

    <!-- Campaign Stats -->
    <div class="grid grid-cols-1 md:grid-cols-5 gap-4">
      <Card class="scale-in hover-lift" style="animation-delay: 0.1s">
        <div class="text-center">
          <p class="text-3xl font-display text-primary-navy">{{ activeCampaigns }}</p>
          <p class="text-sm text-gray-500">Active Campaigns</p>
        </div>
      </Card>
      <Card class="scale-in hover-lift" style="animation-delay: 0.2s">
        <div class="text-center">
          <p class="text-3xl font-display text-primary-emerald">${{ totalRaised.toLocaleString() }}</p>
          <p class="text-sm text-gray-500">Total Raised</p>
        </div>
      </Card>
      <Card class="scale-in hover-lift" style="animation-delay: 0.3s">
        <div class="text-center">
          <p class="text-3xl font-display text-primary-gold">${{ totalGoal.toLocaleString() }}</p>
          <p class="text-sm text-gray-500">Total Goal</p>
        </div>
      </Card>
      <Card class="scale-in hover-lift" style="animation-delay: 0.4s">
        <div class="text-center">
          <p class="text-3xl font-display text-primary-navy">{{ overallProgress }}%</p>
          <p class="text-sm text-gray-500">Overall Progress</p>
        </div>
      </Card>
      <Card class="scale-in hover-lift" style="animation-delay: 0.5s">
        <div class="text-center">
          <p class="text-3xl font-display text-primary-navy">{{ totalDonors }}</p>
          <p class="text-sm text-gray-500">Total Donors</p>
        </div>
      </Card>
    </div>

    <!-- Campaigns List -->
    <Card class="fade-in-up" style="animation-delay: 0.6s" hoverable>
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-lg font-display text-primary-navy">All Campaigns</h3>
        <div class="flex gap-2">
          <select v-model="filterStatus" class="input-field w-40">
            <option value="">All Status</option>
            <option value="active">Active</option>
            <option value="draft">Draft</option>
            <option value="completed">Completed</option>
          </select>
          <select v-model="filterType" class="input-field w-40">
            <option value="">All Types</option>
            <option value="ramadan">Ramadan</option>
            <option value="dhul_hijjah">Dhul Hijjah</option>
            <option value="general">General</option>
            <option value="annual">Annual</option>
          </select>
          <select v-model="sortBy" class="input-field w-40">
            <option value="date">Sort by Date</option>
            <option value="progress">Sort by Progress</option>
            <option value="raised">Sort by Amount</option>
            <option value="donors">Sort by Donors</option>
          </select>
        </div>
      </div>
      
      <div class="space-y-4">
        <div v-for="(campaign, index) in sortedCampaigns" :key="campaign.id" class="p-4 border border-gray-200 rounded-lg hover:border-primary-gold transition-all hover:shadow-md hover:-translate-y-1" style="animation-delay: `${0.7 + index * 0.1}s`">
          <div class="flex items-start justify-between mb-3">
            <div>
              <div class="flex items-center gap-2">
                <h4 class="font-medium text-primary-navy">{{ campaign.name }}</h4>
                <Badge v-if="campaign.isIslamic" variant="success" size="sm">Islamic</Badge>
                <Badge :variant="getStatusVariant(campaign.status)" size="sm">{{ campaign.status }}</Badge>
                <Badge v-if="campaign.trending" variant="primary" size="sm">🔥 Trending</Badge>
              </div>
              <p class="text-sm text-gray-500 mt-1">{{ campaign.type }} • {{ campaign.dateRange }}</p>
            </div>
            <div class="flex gap-2">
              <Button variant="ghost" size="sm" class="ripple" @click="viewCampaign(campaign.id)">
                View
              </Button>
              <Button variant="ghost" size="sm" class="ripple" @click="editCampaign(campaign.id)">
                Edit
              </Button>
              <Button variant="ghost" size="sm" class="ripple" @click="deleteCampaign(campaign.id)">
                Delete
              </Button>
              <Button variant="ghost" size="sm" class="ripple" @click="duplicateCampaign(campaign.id)">
                Duplicate
              </Button>
            </div>
          </div>
          
          <div class="space-y-2">
            <div class="flex items-center justify-between text-sm">
              <span class="text-gray-600">${{ campaign.raised.toLocaleString() }} raised</span>
              <span class="text-gray-600">${{ campaign.goal.toLocaleString() }} goal</span>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-2">
              <div 
                class="bg-primary-gold h-2 rounded-full transition-all duration-500 shimmer"
                :style="{ width: campaign.progress + '%' }"
              />
            </div>
            <div class="flex items-center justify-between text-xs text-gray-500">
              <span>{{ campaign.progress }}% complete</span>
              <span>{{ campaign.donorCount }} donors</span>
              <span v-if="campaign.daysRemaining">{{ campaign.daysRemaining }} days remaining</span>
            </div>
          </div>
          
          <!-- Campaign Performance Metrics -->
          <div class="mt-4 pt-4 border-t border-gray-100 grid grid-cols-4 gap-4 text-center">
            <div>
              <p class="text-lg font-semibold text-primary-navy">${{ campaign.avgDonation.toLocaleString() }}</p>
              <p class="text-xs text-gray-500">Avg Donation</p>
            </div>
            <div>
              <p class="text-lg font-semibold text-primary-emerald">{{ campaign.conversionRate }}%</p>
              <p class="text-xs text-gray-500">Conversion</p>
            </div>
            <div>
              <p class="text-lg font-semibold text-primary-gold">{{ campaign.donationCount }}</p>
              <p class="text-xs text-gray-500">Donations</p>
            </div>
            <div>
              <p class="text-lg font-semibold text-primary-navy">{{ campaign.shareRate }}%</p>
              <p class="text-xs text-gray-500">Share Rate</p>
            </div>
          </div>
        </div>
      </div>
    </Card>

    <!-- Create/Edit Campaign Modal -->
    <Modal :isOpen="showCreateModal" @close="showCreateModal = false">
      <template #header>
        <h2 class="text-xl font-display text-primary-navy">{{ editingCampaign ? 'Edit Campaign' : 'Create New Campaign' }}</h2>
      </template>
      
      <form @submit.prevent="handleCreate" class="space-y-4">
        <div>
          <label class="block text-sm font-medium mb-2">Campaign Name</label>
          <input v-model="newCampaign.name" class="input-field" required />
        </div>
        
        <div>
          <label class="block text-sm font-medium mb-2">Campaign Type</label>
          <select v-model="newCampaign.type" class="input-field">
            <option value="general">General</option>
            <option value="ramadan">Ramadan</option>
            <option value="dhul_hijjah">Dhul Hijjah</option>
            <option value="annual">Annual Fund</option>
            <option value="event">Event-based</option>
            <option value="gasso">GaSSO Scholarship</option>
          </select>
        </div>
        
        <div>
          <label class="block text-sm font-medium mb-2">Status</label>
          <select v-model="newCampaign.status" class="input-field">
            <option value="draft">Draft</option>
            <option value="active">Active</option>
            <option value="completed">Completed</option>
            <option value="archived">Archived</option>
          </select>
        </div>
        
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium mb-2">Start Date</label>
            <input type="date" v-model="newCampaign.startDate" class="input-field" required />
          </div>
          <div>
            <label class="block text-sm font-medium mb-2">End Date</label>
            <input type="date" v-model="newCampaign.endDate" class="input-field" required />
          </div>
        </div>
        
        <div>
          <label class="block text-sm font-medium mb-2">Goal Amount ($)</label>
          <input type="number" v-model="newCampaign.goal" class="input-field" required />
        </div>
        
        <div v-if="newCampaign.type === 'ramadan' || newCampaign.type === 'dhul_hijjah'" class="p-4 bg-primary-gray rounded-lg">
          <p class="text-sm font-medium text-primary-navy mb-2">Islamic Calendar Settings</p>
          <p class="text-xs text-gray-500 mb-2">This campaign will automatically sync with Hijri calendar dates</p>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium mb-1">Hijri Start</label>
              <input type="text" v-model="newCampaign.hijriStart" placeholder="e.g., 1 Ramadan 1447" class="input-field" />
            </div>
            <div>
              <label class="block text-sm font-medium mb-1">Hijri End</label>
              <input type="text" v-model="newCampaign.hijriEnd" placeholder="e.g., 30 Ramadan 1447" class="input-field" />
            </div>
          </div>
        </div>
        
        <label class="flex items-center gap-2">
          <input type="checkbox" v-model="newCampaign.isIslamic" />
          <span class="text-sm">Enable Islamic calendar integration</span>
        </label>
        
        <div class="flex gap-2">
          <Button type="button" variant="ghost" @click="showCreateModal = false">Cancel</Button>
          <Button type="submit" variant="primary">{{ editingCampaign ? 'Update' : 'Create' }} Campaign</Button>
        </div>
      </form>
    </Modal>
  </div>
</template>

<script setup lang="ts">
import Card from '~/components/ui/Card.vue'
import Button from '~/components/ui/Button.vue'
import Input from '~/components/ui/Input.vue'
import Badge from '~/components/ui/Badge.vue'
import Modal from '~/components/ui/Modal.vue'
import { useHijriDate } from '~/composables/useHijriDate'

const { dualDate, inRamadan, inDhulHijjah } = useHijriDate()

const currentHijriDate = computed(() => dualDate.value.hijri)
const isRamadan = computed(() => inRamadan.value)
const isDhulHijjah = computed(() => inDhulHijjah.value)

// Mock campaign data
const campaigns = ref([
  {
    id: '1',
    name: 'Ramadan 2026',
    type: 'ramadan',
    status: 'active',
    isIslamic: true,
    goal: 100000,
    raised: 85000,
    progress: 85,
    donorCount: 234,
    donationCount: 456,
    avgDonation: 186,
    conversionRate: 12,
    shareRate: 8,
    daysRemaining: 15,
    trending: true,
    dateRange: 'Mar 1 - Mar 30, 2026'
  },
  {
    id: '2',
    name: 'Annual Fund 2026',
    type: 'annual',
    status: 'active',
    isIslamic: false,
    goal: 75000,
    raised: 42500,
    progress: 57,
    donorCount: 156,
    donationCount: 289,
    avgDonation: 147,
    conversionRate: 9,
    shareRate: 5,
    daysRemaining: 180,
    trending: false,
    dateRange: 'Jan 1 - Dec 31, 2026'
  },
  {
    id: '3',
    name: 'Building Expansion',
    type: 'general',
    status: 'active',
    isIslamic: false,
    goal: 500000,
    raised: 150000,
    progress: 30,
    donorCount: 45,
    donationCount: 67,
    avgDonation: 2239,
    conversionRate: 15,
    shareRate: 12,
    daysRemaining: 365,
    trending: true,
    dateRange: 'Jan 1, 2026 - Ongoing'
  },
  {
    id: '4',
    name: 'Dhul Hijjah 2025',
    type: 'dhul_hijjah',
    status: 'completed',
    isIslamic: true,
    goal: 50000,
    raised: 52000,
    progress: 104,
    donorCount: 189,
    donationCount: 312,
    avgDonation: 167,
    conversionRate: 18,
    shareRate: 10,
    daysRemaining: 0,
    trending: false,
    dateRange: 'Jun 6 - Jul 6, 2025'
  }
])

const filterStatus = ref('')
const filterType = ref('')
const sortBy = ref('date')
const showCreateModal = ref(false)
const editingCampaign = ref<any>(null)

const newCampaign = ref({
  name: '',
  type: 'general',
  status: 'draft',
  startDate: '',
  endDate: '',
  goal: 0,
  isIslamic: false,
  hijriStart: '',
  hijriEnd: ''
})

const filteredCampaigns = computed(() => {
  return campaigns.value.filter(campaign => {
    const matchesStatus = !filterStatus.value || campaign.status === filterStatus.value
    const matchesType = !filterType.value || campaign.type === filterType.value
    return matchesStatus && matchesType
  })
})

const sortedCampaigns = computed(() => {
  const filtered = filteredCampaigns.value
  return [...filtered].sort((a, b) => {
    switch (sortBy.value) {
      case 'progress':
        return b.progress - a.progress
      case 'raised':
        return b.raised - a.raised
      case 'donors':
        return b.donorCount - a.donorCount
      default:
        return 0 // Keep original order
    }
  })
})

const activeCampaigns = computed(() => campaigns.value.filter(c => c.status === 'active').length)
const totalRaised = computed(() => campaigns.value.reduce((sum, c) => sum + c.raised, 0))
const totalGoal = computed(() => campaigns.value.reduce((sum, c) => sum + c.goal, 0))
const totalDonors = computed(() => campaigns.value.reduce((sum, c) => sum + c.donorCount, 0))
const overallProgress = computed(() => {
  if (totalGoal.value === 0) return 0
  return Math.round((totalRaised.value / totalGoal.value) * 100)
})

const getStatusVariant = (status: string) => {
  const variants: Record<string, string> = {
    active: 'success',
    draft: 'neutral',
    completed: 'info',
    archived: 'neutral'
  }
  return variants[status] || 'neutral'
}

const viewCampaign = (id: string) => {
  navigateTo(`/campaigns/${id}`)
}

const editCampaign = (id: string) => {
  const campaign = campaigns.value.find(c => c.id === id)
  if (campaign) {
    editingCampaign.value = campaign
    newCampaign.value = { ...campaign }
    showCreateModal.value = true
  }
}

const deleteCampaign = (id: string) => {
  if (confirm('Are you sure you want to delete this campaign?')) {
    campaigns.value = campaigns.value.filter(c => c.id !== id)
  }
}

const duplicateCampaign = (id: string) => {
  const campaign = campaigns.value.find(c => c.id === id)
  if (campaign) {
    const newCampaign = {
      ...campaign,
      id: Date.now().toString(),
      name: `${campaign.name} (Copy)`,
      status: 'draft',
      raised: 0,
      progress: 0,
      donorCount: 0
    }
    campaigns.value.push(newCampaign)
  }
}

const handleCreate = () => {
  const startDate = new Date(newCampaign.value.startDate)
  const endDate = new Date(newCampaign.value.endDate)
  const dateRange = `${startDate.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })} - ${endDate.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}`
  
  if (editingCampaign.value) {
    // Update existing campaign
    const index = campaigns.value.findIndex(c => c.id === editingCampaign.value.id)
    if (index !== -1) {
      campaigns.value[index] = {
        ...campaigns.value[index],
        name: newCampaign.value.name,
        type: newCampaign.value.type,
        status: newCampaign.value.status,
        goal: newCampaign.value.goal,
        isIslamic: newCampaign.value.isIslamic,
        dateRange
      }
    }
  } else {
    // Create new campaign
    const newId = Date.now().toString()
    campaigns.value.unshift({
      id: newId,
      name: newCampaign.value.name,
      type: newCampaign.value.type,
      status: newCampaign.value.status || 'draft',
      isIslamic: newCampaign.value.isIslamic,
      goal: newCampaign.value.goal,
      raised: 0,
      progress: 0,
      donorCount: 0,
      donationCount: 0,
      avgDonation: 0,
      conversionRate: 0,
      shareRate: 0,
      daysRemaining: 0,
      trending: false,
      dateRange
    })
  }
  
  showCreateModal.value = false
  editingCampaign.value = null
  
  // Reset form
  newCampaign.value = {
    name: '',
    type: 'general',
    status: 'draft',
    startDate: '',
    endDate: '',
    goal: 0,
    isIslamic: false,
    hijriStart: '',
    hijriEnd: ''
  }
}
</script>
