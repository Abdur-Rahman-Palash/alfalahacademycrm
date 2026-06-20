<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-display text-primary-navy">Email Builder</h1>
        <p class="text-gray-500">Create templates, manage campaigns, and segment donors</p>
      </div>
      <Button variant="primary" @click="showCreateModal = true">
        + Create Email Campaign
      </Button>
    </div>

    <!-- Email Stats -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
      <Card class="scale-in hover-lift" style="animation-delay: 0.1s">
        <div class="text-center">
          <p class="text-3xl font-display text-primary-navy">{{ totalCampaigns }}</p>
          <p class="text-sm text-gray-500">Total Campaigns</p>
        </div>
      </Card>
      <Card class="scale-in hover-lift" style="animation-delay: 0.2s">
        <div class="text-center">
          <p class="text-3xl font-display text-primary-emerald">{{ totalSent }}</p>
          <p class="text-sm text-gray-500">Emails Sent</p>
        </div>
      </Card>
      <Card class="scale-in hover-lift" style="animation-delay: 0.3s">
        <div class="text-center">
          <p class="text-3xl font-display text-primary-gold">{{ openRate }}%</p>
          <p class="text-sm text-gray-500">Open Rate</p>
        </div>
      </Card>
      <Card class="scale-in hover-lift" style="animation-delay: 0.4s">
        <div class="text-center">
          <p class="text-3xl font-display text-primary-navy">{{ clickRate }}%</p>
          <p class="text-sm text-gray-500">Click Rate</p>
        </div>
      </Card>
    </div>

    <!-- Tabs -->
    <div class="border-b border-gray-200">
      <nav class="flex gap-4">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          @click="activeTab = tab.id"
          :class="[
            'py-2 px-4 border-b-2 font-medium transition-colors',
            activeTab === tab.id
              ? 'border-primary-gold text-primary-gold'
              : 'border-transparent text-gray-500 hover:text-gray-700'
          ]"
        >
          {{ tab.label }}
        </button>
      </nav>
    </div>

    <!-- Campaigns Tab -->
    <div v-if="activeTab === 'campaigns'" class="space-y-4">
      <Card class="fade-in-up" style="animation-delay: 0.5s" hoverable>
        <template #header>
          <div class="flex items-center justify-between">
            <h3 class="text-lg font-display text-primary-navy">Email Campaigns</h3>
            <div class="flex gap-2">
              <select v-model="campaignFilter" class="input-field w-40">
                <option value="">All Status</option>
                <option value="draft">Draft</option>
                <option value="scheduled">Scheduled</option>
                <option value="sent">Sent</option>
              </select>
            </div>
          </div>
        </template>
        <div class="space-y-4">
          <div v-for="campaign in filteredCampaigns" :key="campaign.id" class="p-4 border border-gray-200 rounded-lg hover:border-primary-gold transition-colors">
            <div class="flex items-start justify-between mb-3">
              <div>
                <div class="flex items-center gap-2">
                  <h4 class="font-medium text-primary-navy">{{ campaign.name }}</h4>
                  <Badge :variant="getStatusVariant(campaign.status)" size="sm">{{ campaign.status }}</Badge>
                </div>
                <p class="text-sm text-gray-500 mt-1">{{ campaign.subject }}</p>
              </div>
              <div class="flex gap-2">
                <Button variant="ghost" size="sm" @click="editCampaign(campaign.id)">
                  Edit
                </Button>
                <Button v-if="campaign.status === 'draft'" variant="secondary" size="sm" @click="scheduleCampaign(campaign.id)">
                  Schedule
                </Button>
              </div>
            </div>
            <div class="grid grid-cols-4 gap-4 text-sm">
              <div>
                <p class="text-gray-500">Recipients</p>
                <p class="font-medium">{{ campaign.recipients }}</p>
              </div>
              <div>
                <p class="text-gray-500">Open Rate</p>
                <p class="font-medium">{{ campaign.openRate }}%</p>
              </div>
              <div>
                <p class="text-gray-500">Click Rate</p>
                <p class="font-medium">{{ campaign.clickRate }}%</p>
              </div>
              <div>
                <p class="text-gray-500">Sent</p>
                <p class="font-medium">{{ campaign.sentDate || 'Not sent' }}</p>
              </div>
            </div>
          </div>
        </div>
      </Card>
    </div>

    <!-- Templates Tab -->
    <div v-if="activeTab === 'templates'" class="space-y-4">
      <Card class="fade-in-up" style="animation-delay: 0.5s" hoverable>
        <template #header>
          <div class="flex items-center justify-between">
            <h3 class="text-lg font-display text-primary-navy">Email Templates</h3>
            <Button variant="primary" size="sm" @click="showTemplateModal = true">
              + New Template
            </Button>
          </div>
        </template>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div v-for="template in templates" :key="template.id" class="border border-gray-200 rounded-lg p-4 hover:border-primary-gold transition-colors cursor-pointer">
            <div class="flex items-center justify-between mb-3">
              <Badge :variant="template.category === 'fundraising' ? 'success' : 'info'" size="sm">
                {{ template.category }}
              </Badge>
              <div class="flex gap-1">
                <Button variant="ghost" size="sm" @click="editTemplate(template.id)">
                  Edit
                </Button>
                <Button variant="ghost" size="sm" @click="duplicateTemplate(template.id)">
                  Copy
                </Button>
              </div>
            </div>
            <h4 class="font-medium text-primary-navy mb-2">{{ template.name }}</h4>
            <p class="text-sm text-gray-500">{{ template.description }}</p>
            <p class="text-xs text-gray-400 mt-2">Last used: {{ template.lastUsed }}</p>
          </div>
        </div>
      </Card>
    </div>

    <!-- Segmentation Tab -->
    <div v-if="activeTab === 'segments'" class="space-y-4">
      <Card class="fade-in-up" style="animation-delay: 0.5s" hoverable>
        <template #header>
          <div class="flex items-center justify-between">
            <h3 class="text-lg font-display text-primary-navy">Donor Segments</h3>
            <Button variant="primary" size="sm" @click="showSegmentModal = true">
              + Create Segment
            </Button>
          </div>
        </template>
        <div class="space-y-4">
          <div v-for="segment in segments" :key="segment.id" class="p-4 border border-gray-200 rounded-lg">
            <div class="flex items-start justify-between mb-3">
              <div>
                <div class="flex items-center gap-2">
                  <h4 class="font-medium text-primary-navy">{{ segment.name }}</h4>
                  <Badge variant="primary" size="sm">{{ segment.count }} donors</Badge>
                </div>
                <p class="text-sm text-gray-500 mt-1">{{ segment.description }}</p>
              </div>
              <div class="flex gap-2">
                <Button variant="ghost" size="sm" @click="editSegment(segment.id)">
                  Edit
                </Button>
                <Button variant="ghost" size="sm" @click="viewSegment(segment.id)">
                  View
                </Button>
              </div>
            </div>
            <div class="flex flex-wrap gap-2">
              <span v-for="criteria in segment.criteria" :key="criteria" class="text-xs bg-primary-gray px-2 py-1 rounded">
                {{ criteria }}
              </span>
            </div>
          </div>
        </div>
      </Card>
    </div>

    <!-- Create Campaign Modal -->
    <Modal v-if="showCreateModal" @close="showCreateModal = false" size="large">
      <template #header>
        <h2 class="text-xl font-display text-primary-navy">Create Email Campaign</h2>
      </template>
      <div class="space-y-6">
        <div>
          <label class="block text-sm font-medium mb-2">Campaign Name</label>
          <input v-model="newCampaign.name" type="text" class="input-field" placeholder="e.g., Ramadan Appeal 2026" />
        </div>
        
        <div>
          <label class="block text-sm font-medium mb-2">Subject Line</label>
          <input v-model="newCampaign.subject" type="text" class="input-field" placeholder="Email subject line" />
        </div>
        
        <div>
          <label class="block text-sm font-medium mb-2">Template</label>
          <select v-model="newCampaign.templateId" class="input-field">
            <option value="">Select a template</option>
            <option v-for="template in templates" :key="template.id" :value="template.id">
              {{ template.name }}
            </option>
          </select>
        </div>
        
        <div>
          <label class="block text-sm font-medium mb-2">Recipient Segment</label>
          <select v-model="newCampaign.segmentId" class="input-field">
            <option value="">All donors</option>
            <option v-for="segment in segments" :key="segment.id" :value="segment.id">
              {{ segment.name }} ({{ segment.count }})
            </option>
          </select>
        </div>
        
        <div>
          <label class="block text-sm font-medium mb-2">Email Content</label>
          <textarea v-model="newCampaign.content" class="input-field" rows="8" placeholder="Write your email content here..."></textarea>
        </div>
        
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium mb-2">Schedule</label>
            <select v-model="newCampaign.schedule" class="input-field">
              <option value="now">Send Now</option>
              <option value="later">Schedule for Later</option>
            </select>
          </div>
          <div v-if="newCampaign.schedule === 'later'">
            <label class="block text-sm font-medium mb-2">Send Date & Time</label>
            <input v-model="newCampaign.scheduledDate" type="datetime-local" class="input-field" />
          </div>
        </div>
      </div>
      <template #footer>
        <Button variant="ghost" @click="showCreateModal = false">Save as Draft</Button>
        <Button variant="primary" @click="createCampaign">
          {{ newCampaign.schedule === 'now' ? 'Send Now' : 'Schedule Campaign' }}
        </Button>
      </template>
    </Modal>
  </div>
</template>

<script setup lang="ts">
import Card from '~/components/ui/Card.vue'
import Button from '~/components/ui/Button.vue'
import Badge from '~/components/ui/Badge.vue'
import Modal from '~/components/ui/Modal.vue'

const tabs = [
  { id: 'campaigns', label: 'Campaigns' },
  { id: 'templates', label: 'Templates' },
  { id: 'segments', label: 'Segments' }
]

const activeTab = ref('campaigns')
const campaignFilter = ref('')
const showCreateModal = ref(false)
const showTemplateModal = ref(false)
const showSegmentModal = ref(false)

const newCampaign = ref({
  name: '',
  subject: '',
  templateId: '',
  segmentId: '',
  content: '',
  schedule: 'now',
  scheduledDate: ''
})

// Mock data
const campaigns = ref([
  {
    id: '1',
    name: 'Ramadan Appeal 2026',
    subject: 'Support our Ramadan Campaign',
    status: 'sent',
    recipients: 1234,
    openRate: 45,
    clickRate: 12,
    sentDate: 'Mar 1, 2026'
  },
  {
    id: '2',
    name: 'Annual Fund Update',
    subject: 'Your impact this year',
    status: 'sent',
    recipients: 856,
    openRate: 52,
    clickRate: 18,
    sentDate: 'Feb 15, 2026'
  },
  {
    id: '3',
    name: 'Eid Celebration Invitation',
    subject: 'Join us for Eid al-Fitr',
    status: 'scheduled',
    recipients: 2341,
    openRate: 0,
    clickRate: 0,
    sentDate: 'Apr 10, 2026'
  },
  {
    id: '4',
    name: 'Scholarship Announcement',
    subject: 'New scholarship opportunities',
    status: 'draft',
    recipients: 0,
    openRate: 0,
    clickRate: 0,
    sentDate: null
  }
])

const templates = ref([
  {
    id: '1',
    name: 'Fundraising Appeal',
    description: 'Standard donation request template',
    category: 'fundraising',
    lastUsed: 'Mar 1, 2026'
  },
  {
    id: '2',
    name: 'Event Invitation',
    description: 'Event registration and details',
    category: 'events',
    lastUsed: 'Feb 20, 2026'
  },
  {
    id: '3',
    name: 'Thank You',
    description: 'Donation acknowledgment template',
    category: 'fundraising',
    lastUsed: 'Mar 15, 2026'
  },
  {
    id: '4',
    name: 'Newsletter',
    description: 'Monthly newsletter template',
    category: 'updates',
    lastUsed: 'Mar 1, 2026'
  },
  {
    id: '5',
    name: 'Impact Report',
    description: 'Annual impact summary',
    category: 'updates',
    lastUsed: 'Jan 15, 2026'
  }
])

const segments = ref([
  {
    id: '1',
    name: 'Major Donors',
    description: 'Donors who gave $5,000+ in the last year',
    count: 45,
    criteria: ['Total donations > $5,000', 'Last 12 months']
  },
  {
    id: '2',
    name: 'Monthly Givers',
    description: 'Active recurring donation supporters',
    count: 234,
    criteria: ['Has recurring donation', 'Status: Active']
  },
  {
    id: '3',
    name: 'Lapsed Donors',
    description: 'Donors who have not given in 6+ months',
    count: 156,
    criteria: ['Last donation > 6 months ago', 'Previous donor']
  },
  {
    id: '4',
    name: 'Event Attendees',
    description: 'People who attended events in the last year',
    count: 312,
    criteria: ['Event attendance > 0', 'Last 12 months']
  },
  {
    id: '5',
    name: 'New Donors',
    description: 'First-time donors in the last 3 months',
    count: 89,
    criteria: ['First donation < 3 months ago', 'New donor']
  }
])

const filteredCampaigns = computed(() => {
  return campaigns.value.filter(campaign => {
    return !campaignFilter.value || campaign.status === campaignFilter.value
  })
})

const totalCampaigns = computed(() => campaigns.value.length)
const totalSent = computed(() => campaigns.value.filter(c => c.status === 'sent').reduce((sum, c) => sum + c.recipients, 0))
const openRate = computed(() => {
  const sent = campaigns.value.filter(c => c.status === 'sent')
  if (sent.length === 0) return 0
  return Math.round(sent.reduce((sum, c) => sum + c.openRate, 0) / sent.length)
})
const clickRate = computed(() => {
  const sent = campaigns.value.filter(c => c.status === 'sent')
  if (sent.length === 0) return 0
  return Math.round(sent.reduce((sum, c) => sum + c.clickRate, 0) / sent.length)
})

const getStatusVariant = (status: string) => {
  const variants: Record<string, string> = {
    draft: 'neutral',
    scheduled: 'info',
    sent: 'success',
    failed: 'danger'
  }
  return variants[status] || 'neutral'
}

const editCampaign = (id: string) => {
  console.log('Edit campaign:', id)
}

const scheduleCampaign = (id: string) => {
  console.log('Schedule campaign:', id)
}

const editTemplate = (id: string) => {
  console.log('Edit template:', id)
}

const duplicateTemplate = (id: string) => {
  console.log('Duplicate template:', id)
}

const editSegment = (id: string) => {
  console.log('Edit segment:', id)
}

const viewSegment = (id: string) => {
  console.log('View segment:', id)
}

const createCampaign = () => {
  console.log('Create campaign:', newCampaign.value)
  showCreateModal.value = false
}
</script>
