<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-display text-primary-navy">GaSSO Scholarship Tracking</h1>
        <p class="text-gray-500">Manage pledges, approvals, and funding reconciliation</p>
      </div>
      <Button variant="primary" @click="showCreateModal = true">
        + Add Pledge
      </Button>
    </div>

    <!-- GaSSO Pipeline Stats -->
    <div class="grid grid-cols-1 md:grid-cols-5 gap-4">
      <Card class="scale-in hover-lift" style="animation-delay: 0.1s">
        <div class="text-center">
          <p class="text-3xl font-display text-yellow-600">{{ pledgedCount }}</p>
          <p class="text-sm text-gray-500">Pledged</p>
          <p class="text-xs text-primary-emerald mt-1">${{ pledgedTotal.toLocaleString() }}</p>
        </div>
      </Card>
      <Card class="scale-in hover-lift" style="animation-delay: 0.2s">
        <div class="text-center">
          <p class="text-3xl font-display text-blue-600">{{ approvedCount }}</p>
          <p class="text-sm text-gray-500">Approved</p>
          <p class="text-xs text-primary-emerald mt-1">${{ approvedTotal.toLocaleString() }}</p>
        </div>
      </Card>
      <Card class="scale-in hover-lift" style="animation-delay: 0.3s">
        <div class="text-center">
          <p class="text-3xl font-display text-purple-600">{{ partiallyFundedCount }}</p>
          <p class="text-sm text-gray-500">Partially Funded</p>
          <p class="text-xs text-primary-emerald mt-1">${{ partiallyFundedTotal.toLocaleString() }}</p>
        </div>
      </Card>
      <Card class="scale-in hover-lift" style="animation-delay: 0.4s">
        <div class="text-center">
          <p class="text-3xl font-display text-green-600">{{ fullyFundedCount }}</p>
          <p class="text-sm text-gray-500">Fully Funded</p>
          <p class="text-xs text-primary-emerald mt-1">${{ fullyFundedTotal.toLocaleString() }}</p>
        </div>
      </Card>
      <Card class="scale-in hover-lift" style="animation-delay: 0.5s">
        <div class="text-center">
          <p class="text-3xl font-display text-primary-navy">{{ totalStudents }}</p>
          <p class="text-sm text-gray-500">Total Students</p>
        </div>
      </Card>
    </div>

    <!-- Pipeline Visualization -->
    <Card class="fade-in-up" style="animation-delay: 0.6s" hoverable>
      <template #header>
        <h3 class="text-lg font-display text-primary-navy">Funding Pipeline</h3>
      </template>
      <div class="relative">
        <div class="flex items-center justify-between mb-4">
          <div v-for="stage in pipelineStages" :key="stage.name" class="flex-1 text-center">
            <div 
              :class="[
                'w-16 h-16 mx-auto rounded-full flex items-center justify-center mb-2',
                stage.bgColor
              ]"
            >
              <span class="text-2xl font-bold text-white">{{ stage.count }}</span>
            </div>
            <p class="text-sm font-medium text-gray-700">{{ stage.name }}</p>
            <p class="text-xs text-gray-500">${{ stage.total.toLocaleString() }}</p>
          </div>
        </div>
        <div class="h-2 bg-gray-200 rounded-full overflow-hidden">
          <div class="h-full bg-gradient-to-r from-yellow-400 via-blue-500 via-purple-500 to-green-500"></div>
        </div>
      </div>
    </Card>

    <!-- Reconciliation Report -->
    <Card class="fade-in-up" style="animation-delay: 0.7s" hoverable>
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-lg font-display text-primary-navy">Reconciliation Report</h3>
        <div class="flex gap-2">
          <select v-model="reportPeriod" class="input-field w-40">
            <option value="month">This Month</option>
            <option value="quarter">This Quarter</option>
            <option value="year">This Year</option>
            <option value="all">All Time</option>
          </select>
          <Button variant="secondary" size="sm" @click="exportReport">
            Export
          </Button>
        </div>
      </div>
      
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead>
            <tr class="border-b border-gray-200">
              <th class="text-left py-3 px-4 text-sm font-medium text-gray-600">Student</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-gray-600">Grade</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-gray-600">Pledged</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-gray-600">Approved</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-gray-600">Funded</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-gray-600">Remaining</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-gray-600">Status</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-gray-600">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="record in filteredRecords" :key="record.id" class="border-b border-gray-100 hover:bg-gray-50">
              <td class="py-3 px-4">
                <div>
                  <p class="font-medium text-primary-navy">{{ record.studentName }}</p>
                  <p class="text-xs text-gray-500">{{ record.parentName }}</p>
                </div>
              </td>
              <td class="py-3 px-4 text-sm">{{ record.grade }}</td>
              <td class="py-3 px-4 text-sm font-medium">${{ record.pledgedAmount.toLocaleString() }}</td>
              <td class="py-3 px-4 text-sm font-medium">${{ record.approvedAmount.toLocaleString() }}</td>
              <td class="py-3 px-4 text-sm font-medium">${{ record.fundedAmount.toLocaleString() }}</td>
              <td class="py-3 px-4 text-sm font-medium" :class="record.remainingAmount > 0 ? 'text-orange-600' : 'text-green-600'">
                ${{ record.remainingAmount.toLocaleString() }}
              </td>
              <td class="py-3 px-4">
                <Badge :variant="getStatusVariant(record.status)" size="sm">
                  {{ record.status }}
                </Badge>
              </td>
              <td class="py-3 px-4">
                <div class="flex gap-2">
                  <Button variant="ghost" size="sm" @click="viewDetails(record.id)">
                    View
                  </Button>
                  <Button v-if="record.status === 'approved'" variant="secondary" size="sm" @click="recordPayment(record.id)">
                    Record Payment
                  </Button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </Card>

    <!-- Create Pledge Modal -->
    <Modal v-if="showCreateModal" @close="showCreateModal = false">
      <template #header>
        <h2 class="text-xl font-display text-primary-navy">Add New Pledge</h2>
      </template>
      
      <form @submit.prevent="handleCreate" class="space-y-4">
        <Input label="Student Name" v-model="newPledge.studentName" required />
        <Input label="Parent Name" v-model="newPledge.parentName" required />
        
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium mb-2">Grade</label>
            <select v-model="newPledge.grade" class="input-field" required>
              <option value="">Select Grade</option>
              <option v-for="grade in grades" :key="grade" :value="grade">{{ grade }}</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium mb-2">Academic Year</label>
            <select v-model="newPledge.academicYear" class="input-field" required>
              <option value="2025-2026">2025-2026</option>
              <option value="2026-2027">2026-2027</option>
            </select>
          </div>
        </div>
        
        <Input label="Pledged Amount ($)" type="number" v-model="newPledge.pledgedAmount" required />
        
        <div>
          <label class="block text-sm font-medium mb-2">Pledge Type</label>
          <select v-model="newPledge.pledgeType" class="input-field">
            <option value="full">Full Scholarship</option>
            <option value="partial">Partial Scholarship</option>
            <option value="sponsor">Sponsor Funded</option>
          </select>
        </div>
        
        <div>
          <label class="block text-sm font-medium mb-2">Notes</label>
          <textarea v-model="newPledge.notes" class="input-field" rows="3"></textarea>
        </div>
      </form>
      
      <template #footer>
        <Button variant="ghost" @click="showCreateModal = false">Cancel</Button>
        <Button variant="primary" @click="handleCreate">Create Pledge</Button>
      </template>
    </Modal>

    <!-- Record Payment Modal -->
    <Modal v-if="showPaymentModal" @close="showPaymentModal = false">
      <template #header>
        <h2 class="text-xl font-display text-primary-navy">Record Payment</h2>
      </template>
      
      <form @submit.prevent="handlePayment" class="space-y-4">
        <div class="bg-primary-gray p-4 rounded-lg">
          <p class="text-sm font-medium text-primary-navy">{{ selectedRecord?.studentName }}</p>
          <p class="text-xs text-gray-500">Remaining: ${{ selectedRecord?.remainingAmount.toLocaleString() }}</p>
        </div>
        
        <Input label="Payment Amount ($)" type="number" v-model="payment.amount" required />
        
        <div>
          <label class="block text-sm font-medium mb-2">Payment Method</label>
          <select v-model="payment.method" class="input-field">
            <option value="check">Check</option>
            <option value="cash">Cash</option>
            <option value="online">Online</option>
            <option value="transfer">Bank Transfer</option>
          </select>
        </div>
        
        <Input label="Reference Number" v-model="payment.reference" />
        
        <div>
          <label class="block text-sm font-medium mb-2">Payment Date</label>
          <input type="date" v-model="payment.date" class="input-field" required />
        </div>
        
        <div>
          <label class="block text-sm font-medium mb-2">Notes</label>
          <textarea v-model="payment.notes" class="input-field" rows="2"></textarea>
        </div>
      </form>
      
      <template #footer>
        <Button variant="ghost" @click="showPaymentModal = false">Cancel</Button>
        <Button variant="primary" @click="handlePayment">Record Payment</Button>
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

const grades = ['KG', '1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th', '11th', '12th']

// Mock GaSSO data
const records = ref([
  {
    id: '1',
    studentName: 'Ahmed Hassan',
    parentName: 'Mohammed Hassan',
    grade: '5th',
    academicYear: '2025-2026',
    pledgedAmount: 5000,
    approvedAmount: 5000,
    fundedAmount: 5000,
    remainingAmount: 0,
    status: 'fully_funded',
    pledgeType: 'full',
    notes: 'Full scholarship for academic year'
  },
  {
    id: '2',
    studentName: 'Fatima Ahmed',
    parentName: 'Yusuf Ahmed',
    grade: '3rd',
    academicYear: '2025-2026',
    pledgedAmount: 4500,
    approvedAmount: 4500,
    fundedAmount: 2250,
    remainingAmount: 2250,
    status: 'partially_funded',
    pledgeType: 'partial',
    notes: 'Partial scholarship, second payment due'
  },
  {
    id: '3',
    studentName: 'Omar Khalid',
    parentName: 'Ali Khalid',
    grade: '7th',
    academicYear: '2025-2026',
    pledgedAmount: 6000,
    approvedAmount: 0,
    fundedAmount: 0,
    remainingAmount: 6000,
    status: 'pledged',
    pledgeType: 'full',
    notes: 'Awaiting approval'
  },
  {
    id: '4',
    studentName: 'Aisha Mohammed',
    parentName: 'Ibrahim Mohammed',
    grade: '9th',
    academicYear: '2025-2026',
    pledgedAmount: 5500,
    approvedAmount: 5500,
    fundedAmount: 0,
    remainingAmount: 5500,
    status: 'approved',
    pledgeType: 'sponsor',
    notes: 'Sponsor funded, awaiting payment'
  },
  {
    id: '5',
    studentName: 'Yusuf Ali',
    parentName: 'Hassan Ali',
    grade: '11th',
    academicYear: '2025-2026',
    pledgedAmount: 7000,
    approvedAmount: 7000,
    fundedAmount: 7000,
    remainingAmount: 0,
    status: 'fully_funded',
    pledgeType: 'full',
    notes: 'Full scholarship approved'
  }
])

const filterStatus = ref('')
const reportPeriod = ref('month')
const showCreateModal = ref(false)
const showPaymentModal = ref(false)
const selectedRecord = ref<any>(null)

const newPledge = ref({
  studentName: '',
  parentName: '',
  grade: '',
  academicYear: '2025-2026',
  pledgedAmount: 0,
  pledgeType: 'full',
  notes: ''
})

const payment = ref({
  amount: 0,
  method: 'check',
  reference: '',
  date: '',
  notes: ''
})

const filteredRecords = computed(() => {
  return records.value.filter(record => {
    return !filterStatus.value || record.status === filterStatus.value
  })
})

const pipelineStages = computed(() => [
  {
    name: 'Pledged',
    count: pledgedCount.value,
    total: pledgedTotal.value,
    bgColor: 'bg-yellow-500'
  },
  {
    name: 'Approved',
    count: approvedCount.value,
    total: approvedTotal.value,
    bgColor: 'bg-blue-500'
  },
  {
    name: 'Partially Funded',
    count: partiallyFundedCount.value,
    total: partiallyFundedTotal.value,
    bgColor: 'bg-purple-500'
  },
  {
    name: 'Fully Funded',
    count: fullyFundedCount.value,
    total: fullyFundedTotal.value,
    bgColor: 'bg-green-500'
  }
])

const pledgedCount = computed(() => records.value.filter(r => r.status === 'pledged').length)
const approvedCount = computed(() => records.value.filter(r => r.status === 'approved').length)
const partiallyFundedCount = computed(() => records.value.filter(r => r.status === 'partially_funded').length)
const fullyFundedCount = computed(() => records.value.filter(r => r.status === 'fully_funded').length)
const totalStudents = computed(() => records.value.length)

const pledgedTotal = computed(() => records.value.filter(r => r.status === 'pledged').reduce((sum, r) => sum + r.pledgedAmount, 0))
const approvedTotal = computed(() => records.value.filter(r => r.status === 'approved').reduce((sum, r) => sum + r.approvedAmount, 0))
const partiallyFundedTotal = computed(() => records.value.filter(r => r.status === 'partially_funded').reduce((sum, r) => sum + r.fundedAmount, 0))
const fullyFundedTotal = computed(() => records.value.filter(r => r.status === 'fully_funded').reduce((sum, r) => sum + r.fundedAmount, 0))

const getStatusVariant = (status: string) => {
  const variants: Record<string, string> = {
    pledged: 'warning',
    approved: 'info',
    partially_funded: 'primary',
    fully_funded: 'success',
    cancelled: 'danger'
  }
  return variants[status] || 'neutral'
}

const viewDetails = (id: string) => {
  navigateTo(`/scholarships/${id}`)
}

const recordPayment = (id: string) => {
  selectedRecord.value = records.value.find(r => r.id === id)
  showPaymentModal.value = true
}

const handleCreate = () => {
  const record = {
    id: Date.now().toString(),
    ...newPledge.value,
    approvedAmount: 0,
    fundedAmount: 0,
    remainingAmount: newPledge.value.pledgedAmount,
    status: 'pledged'
  }
  records.value.push(record)
  showCreateModal.value = false
}

const handlePayment = () => {
  if (selectedRecord.value) {
    selectedRecord.value.fundedAmount += payment.value.amount
    selectedRecord.value.remainingAmount -= payment.value.amount
    
    if (selectedRecord.value.remainingAmount === 0) {
      selectedRecord.value.status = 'fully_funded'
    } else {
      selectedRecord.value.status = 'partially_funded'
    }
    
    showPaymentModal.value = false
  }
}

const exportReport = () => {
  // TODO: Implement Excel/PDF export
  console.log('Exporting report for period:', reportPeriod.value)
}
</script>
