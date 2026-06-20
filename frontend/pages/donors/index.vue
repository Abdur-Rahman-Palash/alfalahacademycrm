<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-display text-primary-navy">Donors</h1>
        <p class="text-gray-500">Manage constituents and donor information</p>
      </div>
      <Button variant="primary" @click="showAddModal = true">
        + Add Donor
      </Button>
    </div>

    <!-- Filters -->
    <Card>
      <div class="flex gap-4">
        <Input
          v-model="searchQuery"
          placeholder="Search donors..."
          class="flex-1"
        />
        <select v-model="filterType" class="input-field w-48">
          <option value="">All Types</option>
          <option value="individual">Individual</option>
          <option value="family">Family</option>
          <option value="corporate">Corporate</option>
          <option value="foundation">Foundation</option>
        </select>
        <select v-model="filterStatus" class="input-field w-48">
          <option value="">All Status</option>
          <option value="donor">Donors Only</option>
          <option value="parent">Parents Only</option>
          <option value="alumni">Alumni Only</option>
        </select>
      </div>
    </Card>

    <!-- Donors Table -->
    <Card>
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead>
            <tr class="border-b border-gray-200">
              <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Name</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Type</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Email</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Lifetime Giving</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Badges</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="donor in filteredDonors" :key="donor.id" class="border-b border-gray-100 hover:bg-primary-gray/50">
              <td class="py-3 px-4">
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 rounded-full bg-primary-navy flex items-center justify-center text-white font-medium">
                    {{ donor.initials }}
                  </div>
                  <div>
                    <p class="font-medium text-gray-900">{{ donor.name }}</p>
                    <p class="text-sm text-gray-500">{{ donor.orgName || '' }}</p>
                  </div>
                </div>
              </td>
              <td class="py-3 px-4">
                <Badge variant="neutral">{{ donor.type }}</Badge>
              </td>
              <td class="py-3 px-4 text-sm text-gray-600">{{ donor.email }}</td>
              <td class="py-3 px-4 text-sm font-medium text-primary-emerald">${{ donor.lifetimeGiving.toLocaleString() }}</td>
              <td class="py-3 px-4">
                <div class="flex gap-1 flex-wrap">
                  <Badge v-if="donor.isDonor" variant="success" size="sm">Donor</Badge>
                  <Badge v-if="donor.isParent" variant="info" size="sm">Parent</Badge>
                  <Badge v-if="donor.isAlumni" variant="warning" size="sm">Alumni</Badge>
                  <Badge v-if="donor.isVolunteer" variant="neutral" size="sm">Volunteer</Badge>
                </div>
              </td>
              <td class="py-3 px-4">
                <div class="flex gap-2">
                  <Button variant="ghost" size="sm" @click="viewDonor(donor.id)">
                    View
                  </Button>
                  <Button variant="ghost" size="sm" @click="editDonor(donor.id)">
                    Edit
                  </Button>
                  <Button variant="ghost" size="sm" @click="deleteDonor(donor.id)">
                    Delete
                  </Button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <!-- Pagination -->
      <div class="flex items-center justify-between mt-4 pt-4 border-t border-gray-200">
        <p class="text-sm text-gray-500">
          Showing {{ filteredDonors.length }} of {{ donors.length }} donors
        </p>
        <div class="flex gap-2">
          <Button variant="ghost" size="sm" :disabled="currentPage === 1" @click="currentPage--">
            Previous
          </Button>
          <Button variant="ghost" size="sm" :disabled="currentPage >= totalPages" @click="currentPage++">
            Next
          </Button>
        </div>
      </div>
    </Card>

    <!-- Add/Edit Modal -->
    <Modal :isOpen="showAddModal" @close="showAddModal = false">
      <template #header>
        <h2 class="text-xl font-display text-primary-navy">{{ editingDonor ? 'Edit Donor' : 'Add New Donor' }}</h2>
      </template>
      
      <form id="donorForm" @submit.prevent="handleSave" class="space-y-4">
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium mb-2">First Name</label>
            <input v-model="newDonor.firstName" class="input-field" required />
          </div>
          <div>
            <label class="block text-sm font-medium mb-2">Last Name</label>
            <input v-model="newDonor.lastName" class="input-field" required />
          </div>
        </div>
        
        <div>
          <label class="block text-sm font-medium mb-2">Organization Name</label>
          <input v-model="newDonor.orgName" class="input-field" />
        </div>
        <div>
          <label class="block text-sm font-medium mb-2">Email</label>
          <input type="email" v-model="newDonor.email" class="input-field" required />
        </div>
        <div>
          <label class="block text-sm font-medium mb-2">Phone</label>
          <input v-model="newDonor.phone" class="input-field" />
        </div>
        
        <div>
          <label class="block text-sm font-medium mb-2">Type</label>
          <select v-model="newDonor.type" class="input-field">
            <option value="individual">Individual</option>
            <option value="family">Family</option>
            <option value="corporate">Corporate</option>
            <option value="foundation">Foundation</option>
          </select>
        </div>
        
        <div class="flex gap-4">
          <label class="flex items-center gap-2">
            <input type="checkbox" v-model="newDonor.isDonor" />
            <span class="text-sm">Donor</span>
          </label>
          <label class="flex items-center gap-2">
            <input type="checkbox" v-model="newDonor.isParent" />
            <span class="text-sm">Parent</span>
          </label>
          <label class="flex items-center gap-2">
            <input type="checkbox" v-model="newDonor.isAlumni" />
            <span class="text-sm">Alumni</span>
          </label>
          <label class="flex items-center gap-2">
            <input type="checkbox" v-model="newDonor.isVolunteer" />
            <span class="text-sm">Volunteer</span>
          </label>
        </div>
        
        <div class="flex gap-2">
          <Button type="button" variant="ghost" @click="showAddModal = false">Cancel</Button>
          <Button type="submit" variant="primary">{{ editingDonor ? 'Update' : 'Save' }} Donor</Button>
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

interface Donor {
  id: string
  name: string
  initials: string
  orgName?: string
  email: string
  type: string
  lifetimeGiving: number
  isDonor: boolean
  isParent: boolean
  isAlumni: boolean
  isVolunteer: boolean
}

// Mock data - replace with API call
const donors = ref<Donor[]>([
  {
    id: '1',
    name: 'Ahmed Family',
    initials: 'AF',
    email: 'ahmed.family@example.com',
    type: 'family',
    lifetimeGiving: 15000,
    isDonor: true,
    isParent: true,
    isAlumni: false,
    isVolunteer: false
  },
  {
    id: '2',
    name: 'Mohammed Corporation',
    initials: 'MC',
    orgName: 'Mohammed Corp',
    email: 'contact@mohammedcorp.com',
    type: 'corporate',
    lifetimeGiving: 50000,
    isDonor: true,
    isParent: false,
    isAlumni: false,
    isVolunteer: false
  },
  {
    id: '3',
    name: 'Sarah Khan',
    initials: 'SK',
    email: 'sarah.khan@example.com',
    type: 'individual',
    lifetimeGiving: 2500,
    isDonor: true,
    isParent: false,
    isAlumni: true,
    isVolunteer: true
  },
  {
    id: '4',
    name: 'Omar Foundation',
    initials: 'OF',
    orgName: 'Omar Foundation',
    email: 'info@omarfoundation.org',
    type: 'foundation',
    lifetimeGiving: 100000,
    isDonor: true,
    isParent: false,
    isAlumni: false,
    isVolunteer: false
  }
])

const searchQuery = ref('')
const filterType = ref('')
const filterStatus = ref('')
const currentPage = ref(1)
const showAddModal = ref(false)
const editingDonor = ref<Donor | null>(null)

const newDonor = ref({
  firstName: '',
  lastName: '',
  orgName: '',
  email: '',
  phone: '',
  type: 'individual',
  isDonor: false,
  isParent: false,
  isAlumni: false,
  isVolunteer: false
})

const filteredDonors = computed(() => {
  return donors.value.filter(donor => {
    const matchesSearch = donor.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                         donor.email.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesType = !filterType.value || donor.type === filterType.value
    const matchesStatus = !filterStatus.value || 
                         (filterStatus.value === 'donor' && donor.isDonor) ||
                         (filterStatus.value === 'parent' && donor.isParent) ||
                         (filterStatus.value === 'alumni' && donor.isAlumni)
    
    return matchesSearch && matchesType && matchesStatus
  })
})

const totalPages = computed(() => Math.ceil(filteredDonors.value.length / 10))

const viewDonor = (id: string) => {
  navigateTo(`/donors/${id}`)
}

const editDonor = (id: string) => {
  const donor = donors.value.find(d => d.id === id)
  if (donor) {
    editingDonor.value = donor
    newDonor.value = {
      firstName: donor.name.split(' ')[0] || '',
      lastName: donor.name.split(' ').slice(1).join(' ') || '',
      orgName: donor.orgName || '',
      email: donor.email,
      phone: '',
      type: donor.type,
      isDonor: donor.isDonor,
      isParent: donor.isParent,
      isAlumni: donor.isAlumni,
      isVolunteer: donor.isVolunteer
    }
    showAddModal.value = true
  }
}

const deleteDonor = (id: string) => {
  if (confirm('Are you sure you want to delete this donor?')) {
    donors.value = donors.value.filter(d => d.id !== id)
  }
}

const handleSave = () => {
  const name = newDonor.value.orgName || `${newDonor.value.firstName} ${newDonor.value.lastName}`
  const initials = name.split(' ').map(n => n[0]).join('').toUpperCase()
  
  if (editingDonor.value) {
    // Update existing donor
    const index = donors.value.findIndex(d => d.id === editingDonor.value.id)
    if (index !== -1) {
      donors.value[index] = {
        ...donors.value[index],
        name,
        initials,
        orgName: newDonor.value.orgName,
        email: newDonor.value.email,
        type: newDonor.value.type,
        isDonor: newDonor.value.isDonor,
        isParent: newDonor.value.isParent,
        isAlumni: newDonor.value.isAlumni,
        isVolunteer: newDonor.value.isVolunteer
      }
    }
  } else {
    // Add new donor
    const newId = Date.now().toString()
    donors.value.unshift({
      id: newId,
      name,
      initials,
      orgName: newDonor.value.orgName,
      email: newDonor.value.email,
      type: newDonor.value.type,
      lifetimeGiving: 0,
      isDonor: newDonor.value.isDonor,
      isParent: newDonor.value.isParent,
      isAlumni: newDonor.value.isAlumni,
      isVolunteer: newDonor.value.isVolunteer
    })
  }
  
  showAddModal.value = false
  editingDonor.value = null
  
  // Reset form
  newDonor.value = {
    firstName: '',
    lastName: '',
    orgName: '',
    email: '',
    phone: '',
    type: 'individual',
    isDonor: false,
    isParent: false,
    isAlumni: false,
    isVolunteer: false
  }
}
</script>
