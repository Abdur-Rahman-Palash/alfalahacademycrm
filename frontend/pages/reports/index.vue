<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-display text-primary-navy">Reports & Analytics</h1>
        <p class="text-gray-500">Generate reports and export data in multiple formats</p>
      </div>
      <Button variant="primary" @click="showCreateReportModal = true">
        + Create Custom Report
      </Button>
    </div>

    <!-- Report Categories -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
      <Card class="scale-in hover-lift cursor-pointer" style="animation-delay: 0.1s" @click="filterByCategory('donations')">
        <div class="text-center">
          <div class="w-12 h-12 bg-primary-gold/20 rounded-full flex items-center justify-center mx-auto mb-3">
            <span class="text-2xl">💰</span>
          </div>
          <h4 class="font-semibold text-primary-navy mb-1">Donation Reports</h4>
          <p class="text-sm text-gray-500">Financial analysis</p>
        </div>
      </Card>
      
      <Card class="scale-in hover-lift cursor-pointer" style="animation-delay: 0.2s" @click="filterByCategory('donors')">
        <div class="text-center">
          <div class="w-12 h-12 bg-primary-emerald/20 rounded-full flex items-center justify-center mx-auto mb-3">
            <span class="text-2xl">👥</span>
          </div>
          <h4 class="font-semibold text-primary-navy mb-1">Donor Reports</h4>
          <p class="text-sm text-gray-500">Constituent analysis</p>
        </div>
      </Card>
      
      <Card class="scale-in hover-lift cursor-pointer" style="animation-delay: 0.3s" @click="filterByCategory('campaigns')">
        <div class="text-center">
          <div class="w-12 h-12 bg-primary-navy/20 rounded-full flex items-center justify-center mx-auto mb-3">
            <span class="text-2xl">🎯</span>
          </div>
          <h4 class="font-semibold text-primary-navy mb-1">Campaign Reports</h4>
          <p class="text-sm text-gray-500">Campaign performance</p>
        </div>
      </Card>
      
      <Card class="scale-in hover-lift cursor-pointer" style="animation-delay: 0.4s" @click="filterByCategory('events')">
        <div class="text-center">
          <div class="w-12 h-12 bg-primary-gold/20 rounded-full flex items-center justify-center mx-auto mb-3">
            <span class="text-2xl">📅</span>
          </div>
          <h4 class="font-semibold text-primary-navy mb-1">Event Reports</h4>
          <p class="text-sm text-gray-500">Event analytics</p>
        </div>
      </Card>
    </div>

    <!-- Available Reports -->
    <Card class="fade-in-up" style="animation-delay: 0.5s" hoverable>
      <template #header>
        <div class="flex items-center justify-between">
          <h3 class="text-lg font-display text-primary-navy">Available Reports</h3>
          <div class="flex gap-2">
            <select v-model="dateRange" class="input-field w-40">
              <option value="30">Last 30 Days</option>
              <option value="90">Last 90 Days</option>
              <option value="365">Last Year</option>
              <option value="all">All Time</option>
            </select>
            <select v-model="categoryFilter" class="input-field w-40">
              <option value="">All Categories</option>
              <option value="donations">Donations</option>
              <option value="donors">Donors</option>
              <option value="campaigns">Campaigns</option>
              <option value="events">Events</option>
            </select>
          </div>
        </div>
      </template>
      
      <div class="space-y-4">
        <div v-for="report in filteredReports" :key="report.id" class="p-4 border border-gray-200 rounded-lg hover:border-primary-gold transition-colors">
          <div class="flex items-start justify-between mb-3">
            <div class="flex items-start gap-4">
              <div class="w-10 h-10 rounded-full flex items-center justify-center" :class="report.iconBg">
                <span class="text-xl">{{ report.icon }}</span>
              </div>
              <div>
                <h4 class="font-medium text-primary-navy">{{ report.name }}</h4>
                <p class="text-sm text-gray-500">{{ report.description }}</p>
                <div class="flex items-center gap-2 mt-2">
                  <Badge variant="neutral" size="sm">{{ report.category }}</Badge>
                  <span class="text-xs text-gray-400">Last updated: {{ report.lastUpdated }}</span>
                </div>
              </div>
            </div>
            <div class="flex gap-2">
              <Button variant="ghost" size="sm" @click="viewReport(report.id)">
                View
              </Button>
              <Button variant="secondary" size="sm" @click="exportReport(report.id, 'excel')">
                Excel
              </Button>
              <Button variant="secondary" size="sm" @click="exportReport(report.id, 'pdf')">
                PDF
              </Button>
            </div>
          </div>
        </div>
      </div>
    </Card>

    <!-- Scheduled Reports -->
    <Card class="fade-in-up" style="animation-delay: 0.6s" hoverable>
      <template #header>
        <div class="flex items-center justify-between">
          <h3 class="text-lg font-display text-primary-navy">Scheduled Reports</h3>
          <Button variant="primary" size="sm" @click="showScheduleModal = true">
            + Schedule Report
          </Button>
        </div>
      </template>
      
      <div class="space-y-4">
        <div v-for="scheduled in scheduledReports" :key="scheduled.id" class="p-4 border border-gray-200 rounded-lg">
          <div class="flex items-start justify-between mb-3">
            <div>
              <div class="flex items-center gap-2">
                <h4 class="font-medium text-primary-navy">{{ scheduled.name }}</h4>
                <Badge variant="success" size="sm">Active</Badge>
              </div>
              <p class="text-sm text-gray-500 mt-1">{{ scheduled.frequency }} • Next run: {{ scheduled.nextRun }}</p>
            </div>
            <div class="flex gap-2">
              <Button variant="ghost" size="sm" @click="editSchedule(scheduled.id)">
                Edit
              </Button>
              <Button variant="ghost" size="sm" @click="pauseSchedule(scheduled.id)">
                Pause
              </Button>
            </div>
          </div>
          <div class="flex items-center gap-4 text-sm text-gray-500">
            <span>Recipients: {{ scheduled.recipients.join(', ') }}</span>
            <span>Format: {{ scheduled.format }}</span>
          </div>
        </div>
      </div>
    </Card>

    <!-- Custom Report Builder Modal -->
    <Modal v-if="showCreateReportModal" @close="showCreateReportModal = false" size="large">
      <template #header>
        <h2 class="text-xl font-display text-primary-navy">Create Custom Report</h2>
      </template>
      
      <div class="space-y-6">
        <div>
          <label class="block text-sm font-medium mb-2">Report Name</label>
          <input v-model="customReport.name" type="text" class="input-field" placeholder="e.g., Monthly Donation Summary" />
        </div>
        
        <div>
          <label class="block text-sm font-medium mb-2">Data Source</label>
          <select v-model="customReport.dataSource" class="input-field">
            <option value="donations">Donations</option>
            <option value="donors">Donors</option>
            <option value="campaigns">Campaigns</option>
            <option value="events">Events</option>
            <option value="scholarships">Scholarships</option>
          </select>
        </div>
        
        <div>
          <label class="block text-sm font-medium mb-2">Date Range</label>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-xs text-gray-500 mb-1">Start Date</label>
              <input v-model="customReport.startDate" type="date" class="input-field" />
            </div>
            <div>
              <label class="block text-xs text-gray-500 mb-1">End Date</label>
              <input v-model="customReport.endDate" type="date" class="input-field" />
            </div>
          </div>
        </div>
        
        <div>
          <label class="block text-sm font-medium mb-2">Select Fields</label>
          <div class="grid grid-cols-2 md:grid-cols-3 gap-2">
            <label v-for="field in availableFields" :key="field.value" class="flex items-center gap-2 p-2 border border-gray-200 rounded-lg cursor-pointer hover:border-primary-gold">
              <input type="checkbox" v-model="customReport.selectedFields" :value="field.value" />
              <span class="text-sm">{{ field.label }}</span>
            </label>
          </div>
        </div>
        
        <div>
          <label class="block text-sm font-medium mb-2">Filters</label>
          <div class="space-y-2">
            <div v-for="(filter, index) in customReport.filters" :key="index" class="flex gap-2 items-center">
              <select v-model="filter.field" class="input-field flex-1">
                <option value="">Select field</option>
                <option v-for="field in availableFields" :key="field.value" :value="field.value">
                  {{ field.label }}
                </option>
              </select>
              <select v-model="filter.operator" class="input-field w-32">
                <option value="equals">=</option>
                <option value="not_equals">≠</option>
                <option value="greater">></option>
                <option value="less"><</option>
                <option value="contains">Contains</option>
              </select>
              <input v-model="filter.value" type="text" class="input-field flex-1" placeholder="Value" />
              <Button variant="ghost" size="sm" @click="removeFilter(index)">✕</Button>
            </div>
            <Button variant="ghost" size="sm" @click="addFilter">+ Add Filter</Button>
          </div>
        </div>
        
        <div>
          <label class="block text-sm font-medium mb-2">Group By</label>
          <select v-model="customReport.groupBy" class="input-field">
            <option value="">No grouping</option>
            <option v-for="field in availableFields" :key="field.value" :value="field.value">
              {{ field.label }}
            </option>
          </select>
        </div>
        
        <div>
          <label class="block text-sm font-medium mb-2">Export Format</label>
          <div class="flex gap-4">
            <label class="flex items-center gap-2">
              <input type="radio" v-model="customReport.format" value="excel" />
              <span class="text-sm">Excel</span>
            </label>
            <label class="flex items-center gap-2">
              <input type="radio" v-model="customReport.format" value="pdf" />
              <span class="text-sm">PDF</span>
            </label>
            <label class="flex items-center gap-2">
              <input type="radio" v-model="customReport.format" value="csv" />
              <span class="text-sm">CSV</span>
            </label>
          </div>
        </div>
      </div>
      
      <template #footer>
        <Button variant="ghost" @click="showCreateReportModal = false">Cancel</Button>
        <Button variant="primary" @click="generateCustomReport">
          Generate Report
        </Button>
      </template>
    </Modal>

    <!-- Schedule Report Modal -->
    <Modal v-if="showScheduleModal" @close="showScheduleModal = false">
      <template #header>
        <h2 class="text-xl font-display text-primary-navy">Schedule Report</h2>
      </template>
      
      <div class="space-y-4">
        <div>
          <label class="block text-sm font-medium mb-2">Report</label>
          <select v-model="scheduledReport.reportId" class="input-field">
            <option value="">Select a report</option>
            <option v-for="report in reports" :key="report.id" :value="report.id">
              {{ report.name }}
            </option>
          </select>
        </div>
        
        <div>
          <label class="block text-sm font-medium mb-2">Frequency</label>
          <select v-model="scheduledReport.frequency" class="input-field">
            <option value="daily">Daily</option>
            <option value="weekly">Weekly</option>
            <option value="monthly">Monthly</option>
            <option value="quarterly">Quarterly</option>
          </select>
        </div>
        
        <div>
          <label class="block text-sm font-medium mb-2">Email Recipients</label>
          <input v-model="scheduledReport.recipients" type="text" class="input-field" placeholder="email1@example.com, email2@example.com" />
        </div>
        
        <div>
          <label class="block text-sm font-medium mb-2">Export Format</label>
          <select v-model="scheduledReport.format" class="input-field">
            <option value="excel">Excel</option>
            <option value="pdf">PDF</option>
          </select>
        </div>
      </div>
      
      <template #footer>
        <Button variant="ghost" @click="showScheduleModal = false">Cancel</Button>
        <Button variant="primary" @click="scheduleReport">
          Schedule Report
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

const dateRange = ref('30')
const categoryFilter = ref('')
const showCreateReportModal = ref(false)
const showScheduleModal = ref(false)

const customReport = ref({
  name: '',
  dataSource: 'donations',
  startDate: '',
  endDate: '',
  selectedFields: [],
  filters: [],
  groupBy: '',
  format: 'excel'
})

const scheduledReport = ref({
  reportId: '',
  frequency: 'monthly',
  recipients: '',
  format: 'excel'
})

const availableFields = ref([
  { label: 'Donor Name', value: 'donor_name' },
  { label: 'Amount', value: 'amount' },
  { label: 'Date', value: 'date' },
  { label: 'Campaign', value: 'campaign' },
  { label: 'Payment Method', value: 'payment_method' },
  { label: 'Donation Type', value: 'donation_type' },
  { label: 'Frequency', value: 'frequency' },
  { label: 'Status', value: 'status' },
  { label: 'Email', value: 'email' },
  { label: 'Phone', value: 'phone' },
  { label: 'Address', value: 'address' },
  { label: 'City', value: 'city' }
])

// Mock data
const reports = ref([
  {
    id: '1',
    name: 'Monthly Donation Summary',
    description: 'Comprehensive monthly donation report with breakdown by campaign and donor type',
    category: 'donations',
    icon: '💰',
    iconBg: 'bg-primary-gold/20',
    lastUpdated: 'Mar 15, 2026'
  },
  {
    id: '2',
    name: 'Donor Retention Analysis',
    description: 'Track donor retention rates and identify lapsed donors',
    category: 'donors',
    icon: '👥',
    iconBg: 'bg-primary-emerald/20',
    lastUpdated: 'Mar 14, 2026'
  },
  {
    id: '3',
    name: 'Campaign Performance Report',
    description: 'Detailed campaign performance metrics and ROI analysis',
    category: 'campaigns',
    icon: '🎯',
    iconBg: 'bg-primary-navy/20',
    lastUpdated: 'Mar 13, 2026'
  },
  {
    id: '4',
    name: 'Event Attendance Report',
    description: 'Event registration, attendance, and revenue analysis',
    category: 'events',
    icon: '📅',
    iconBg: 'bg-primary-gold/20',
    lastUpdated: 'Mar 12, 2026'
  },
  {
    id: '5',
    name: 'Recurring Donation Report',
    description: 'Monthly recurring donation status and payment history',
    category: 'donations',
    icon: '💰',
    iconBg: 'bg-primary-gold/20',
    lastUpdated: 'Mar 15, 2026'
  },
  {
    id: '6',
    name: 'GaSSO Scholarship Report',
    description: 'Scholarship pledge tracking and funding reconciliation',
    category: 'scholarships',
    icon: '🎓',
    iconBg: 'bg-primary-emerald/20',
    lastUpdated: 'Mar 10, 2026'
  }
])

const scheduledReports = ref([
  {
    id: '1',
    name: 'Monthly Donation Summary',
    frequency: 'Monthly',
    nextRun: 'Apr 1, 2026',
    recipients: ['admin@alfalahacademy.com', 'finance@alfalahacademy.com'],
    format: 'Excel'
  },
  {
    id: '2',
    name: 'Weekly Campaign Performance',
    frequency: 'Weekly',
    nextRun: 'Mar 22, 2026',
    recipients: ['admin@alfalahacademy.com'],
    format: 'PDF'
  }
])

const filteredReports = computed(() => {
  return reports.value.filter(report => {
    const matchesCategory = !categoryFilter.value || report.category === categoryFilter.value
    return matchesCategory
  })
})

const filterByCategory = (category: string) => {
  categoryFilter.value = category
}

const viewReport = (id: string) => {
  console.log('View report:', id)
}

const exportReport = (id: string, format: string) => {
  console.log('Export report:', id, format)
}

const addFilter = () => {
  customReport.value.filters.push({ field: '', operator: 'equals', value: '' })
}

const removeFilter = (index: number) => {
  customReport.value.filters.splice(index, 1)
}

const generateCustomReport = () => {
  console.log('Generate custom report:', customReport.value)
  showCreateReportModal.value = false
}

const editSchedule = (id: string) => {
  console.log('Edit schedule:', id)
}

const pauseSchedule = (id: string) => {
  console.log('Pause schedule:', id)
}

const scheduleReport = () => {
  console.log('Schedule report:', scheduledReport.value)
  showScheduleModal.value = false
}
</script>
