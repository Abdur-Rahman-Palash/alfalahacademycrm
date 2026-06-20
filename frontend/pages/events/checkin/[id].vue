<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-display text-primary-navy">Event Check-in</h1>
        <p class="text-gray-500">{{ event.name }}</p>
      </div>
      <Button variant="secondary" @click="navigateTo('/events')">
        ← Back to Events
      </Button>
    </div>

    <!-- Stats -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <Card>
        <div class="text-center">
          <p class="text-3xl font-display text-primary-navy">{{ checkedInCount }}</p>
          <p class="text-sm text-gray-500">Checked In</p>
        </div>
      </Card>
      <Card>
        <div class="text-center">
          <p class="text-3xl font-display text-primary-emerald">{{ remainingCount }}</p>
          <p class="text-sm text-gray-500">Remaining</p>
        </div>
      </Card>
      <Card>
        <div class="text-center">
          <p class="text-3xl font-display text-primary-gold">{{ totalRegistrations }}</p>
          <p class="text-sm text-gray-500">Total</p>
        </div>
      </Card>
    </div>

    <!-- QR Scanner -->
    <Card>
      <template #header>
        <h3 class="text-lg font-display text-primary-navy">Scan QR Code</h3>
      </template>
      
      <div class="space-y-4">
        <div class="bg-black aspect-video rounded-lg flex items-center justify-center">
          <p class="text-white text-center">
            <svg class="w-16 h-16 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v1m6 11h2m-6 0h-2v4m0-11v3m0 0h.01M12 12h4.01M16 20h4M4 12h4m12 0h.01M5 8h2a1 1 0 001-1V5a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1zm12 0h2a1 1 0 001-1V5a1 1 0 00-1-1h-2a1 1 0 00-1 1v2a1 1 0 001 1zM5 20h2a1 1 0 001-1v-2a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1z" />
            </svg>
            Camera will activate here
          </p>
        </div>
        
        <div>
          <label class="block text-sm font-medium mb-2">Or enter ticket code manually</label>
          <div class="flex gap-2">
            <Input v-model="manualCode" placeholder="Enter QR code" class="flex-1" />
            <Button variant="primary" @click="handleManualCheckIn">
              Check In
            </Button>
          </div>
        </div>
      </div>
    </Card>

    <!-- Recent Check-ins -->
    <Card>
      <template #header>
        <h3 class="text-lg font-display text-primary-navy">Recent Check-ins</h3>
      </template>
      
      <div class="space-y-3">
        <div v-for="checkIn in recentCheckIns" :key="checkIn.id" class="flex items-center gap-4 p-3 bg-primary-gray rounded-lg">
          <div class="w-10 h-10 rounded-full bg-primary-navy flex items-center justify-center text-white font-medium">
            {{ checkIn.initials }}
          </div>
          <div class="flex-1">
            <p class="font-medium">{{ checkIn.name }}</p>
            <p class="text-sm text-gray-500">{{ checkIn.ticketType }}</p>
          </div>
          <div class="text-right">
            <p class="text-sm text-gray-500">{{ checkIn.time }}</p>
            <Badge variant="success" size="sm">Checked In</Badge>
          </div>
        </div>
      </div>
    </Card>

    <!-- Attendee List -->
    <Card>
      <template #header>
        <div class="flex items-center justify-between">
          <h3 class="text-lg font-display text-primary-navy">All Attendees</h3>
          <Input v-model="searchQuery" placeholder="Search attendees..." class="w-64" />
        </div>
      </template>
      
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead>
            <tr class="border-b border-gray-200">
              <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Name</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Ticket Type</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Status</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Check-in Time</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="attendee in filteredAttendees" :key="attendee.id" class="border-b border-gray-100 hover:bg-primary-gray/50">
              <td class="py-3 px-4">
                <div class="flex items-center gap-3">
                  <div class="w-8 h-8 rounded-full bg-primary-navy flex items-center justify-center text-white text-sm font-medium">
                    {{ attendee.initials }}
                  </div>
                  <span class="font-medium">{{ attendee.name }}</span>
                </div>
              </td>
              <td class="py-3 px-4 text-sm">{{ attendee.ticketType }}</td>
              <td class="py-3 px-4">
                <Badge :variant="attendee.checkedIn ? 'success' : 'neutral'" size="sm">
                  {{ attendee.checkedIn ? 'Checked In' : 'Pending' }}
                </Badge>
              </td>
              <td class="py-3 px-4 text-sm text-gray-500">{{ attendee.checkInTime || '-' }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </Card>
  </div>
</template>

<script setup lang="ts">
import Card from '~/components/ui/Card.vue'
import Button from '~/components/ui/Button.vue'
import Input from '~/components/ui/Input.vue'
import Badge from '~/components/ui/Badge.vue'

const route = useRoute()
const eventId = route.params.id as string

// Mock event data
const event = ref({
  id: eventId,
  name: 'Annual Gala 2026',
  date: 'August 15, 2026 at 6:00 PM'
})

// Mock attendee data
const attendees = ref([
  { id: '1', name: 'Ahmed Family', initials: 'AF', ticketType: 'VIP', checkedIn: true, checkInTime: '6:05 PM' },
  { id: '2', name: 'Mohammed Corp', initials: 'MC', ticketType: 'Sponsor', checkedIn: true, checkInTime: '6:08 PM' },
  { id: '3', name: 'Sarah Khan', initials: 'SK', ticketType: 'General', checkedIn: false, checkInTime: null },
  { id: '4', name: 'Omar Foundation', initials: 'OF', ticketType: 'Sponsor', checkedIn: false, checkInTime: null },
  { id: '5', name: 'Fatima Ahmed', initials: 'FA', ticketType: 'General', checkedIn: true, checkInTime: '6:12 PM' }
])

const recentCheckIns = ref([
  { id: '1', name: 'Fatima Ahmed', initials: 'FA', ticketType: 'General', time: '6:12 PM' },
  { id: '2', name: 'Mohammed Corp', initials: 'MC', ticketType: 'Sponsor', time: '6:08 PM' },
  { id: '3', name: 'Ahmed Family', initials: 'AF', ticketType: 'VIP', time: '6:05 PM' }
])

const searchQuery = ref('')
const manualCode = ref('')

const checkedInCount = computed(() => attendees.value.filter(a => a.checkedIn).length)
const remainingCount = computed(() => attendees.value.filter(a => !a.checkedIn).length)
const totalRegistrations = computed(() => attendees.value.length)

const filteredAttendees = computed(() => {
  return attendees.value.filter(attendee => {
    return attendee.name.toLowerCase().includes(searchQuery.value.toLowerCase())
  })
})

const handleManualCheckIn = () => {
  // TODO: Implement manual check-in logic
  console.log('Manual check-in for code:', manualCode.value)
  manualCode.value = ''
}
</script>
