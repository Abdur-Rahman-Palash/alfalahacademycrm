<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-display text-primary-navy">Events</h1>
        <p class="text-gray-500">Manage events, ticketing, and check-in</p>
      </div>
      <Button variant="primary" @click="showCreateModal = true">
        + Create Event
      </Button>
    </div>

    <!-- Event Stats -->
    <div class="grid grid-cols-1 md:grid-cols-5 gap-4">
      <Card class="scale-in hover-lift" style="animation-delay: 0.1s">
        <div class="text-center">
          <p class="text-3xl font-display text-primary-navy">{{ upcomingEvents }}</p>
          <p class="text-sm text-gray-500">Upcoming Events</p>
        </div>
      </Card>
      <Card class="scale-in hover-lift" style="animation-delay: 0.2s">
        <div class="text-center">
          <p class="text-3xl font-display text-primary-emerald">{{ totalRegistrations }}</p>
          <p class="text-sm text-gray-500">Total Registrations</p>
        </div>
      </Card>
      <Card class="scale-in hover-lift" style="animation-delay: 0.3s">
        <div class="text-center">
          <p class="text-3xl font-display text-primary-gold">${{ totalRevenue.toLocaleString() }}</p>
          <p class="text-sm text-gray-500">Total Revenue</p>
        </div>
      </Card>
      <Card class="scale-in hover-lift" style="animation-delay: 0.4s">
        <div class="text-center">
          <p class="text-3xl font-display text-primary-navy">{{ checkedIn }}</p>
          <p class="text-sm text-gray-500">Checked In Today</p>
        </div>
      </Card>
      <Card class="scale-in hover-lift" style="animation-delay: 0.5s">
        <div class="text-center">
          <p class="text-3xl font-display text-primary-navy">{{ ticketedEvents }}</p>
          <p class="text-sm text-gray-500">Ticketed Events</p>
        </div>
      </Card>
    </div>

    <!-- Events List -->
    <Card>
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-lg font-display text-primary-navy">All Events</h3>
        <div class="flex gap-2">
          <select v-model="filterStatus" class="input-field w-40">
            <option value="">All Status</option>
            <option value="upcoming">Upcoming</option>
            <option value="live">Live</option>
            <option value="completed">Completed</option>
          </select>
        </div>
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div v-for="event in filteredEvents" :key="event.id" class="border border-gray-200 rounded-lg p-4 hover:border-primary-gold transition-colors">
          <div class="flex items-start justify-between mb-3">
            <Badge :variant="getStatusVariant(event.status)" size="sm">{{ event.status }}</Badge>
            <div class="flex gap-1">
              <span v-if="event.isTicketed" class="text-xs bg-primary-gray px-2 py-1 rounded">Ticketed</span>
              <span v-if="event.hasSponsorship" class="text-xs bg-primary-gold/10 text-primary-gold px-2 py-1 rounded">Sponsorship</span>
            </div>
          </div>
          
          <h4 class="font-medium text-primary-navy mb-2">{{ event.name }}</h4>
          
          <div class="space-y-2 text-sm text-gray-600">
            <div class="flex items-center gap-2">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              <span>{{ event.date }}</span>
            </div>
            <div class="flex items-center gap-2">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
              <span>{{ event.location }}</span>
            </div>
            <div class="flex items-center gap-2">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
              <span>{{ event.registrations }} / {{ event.capacity || '∞' }}</span>
            </div>
          </div>
          
          <div class="flex gap-2 mt-4">
            <Button variant="ghost" size="sm" class="flex-1" @click="viewEvent(event.id)">
              View
            </Button>
            <Button variant="ghost" size="sm" @click="editEvent(event.id)">
              Edit
            </Button>
            <Button variant="ghost" size="sm" @click="deleteEvent(event.id)">
              Delete
            </Button>
            <Button v-if="event.status === 'upcoming' && event.isTicketed" variant="secondary" size="sm" @click="openCheckIn(event.id)">
              Check-in
            </Button>
          </div>
        </div>
      </div>
    </Card>

    <!-- Create/Edit Event Modal -->
    <Modal :isOpen="showCreateModal" @close="showCreateModal = false">
      <template #header>
        <h2 class="text-xl font-display text-primary-navy">{{ editingEvent ? 'Edit Event' : 'Create New Event' }}</h2>
      </template>
      
      <form @submit.prevent="handleCreate" class="space-y-4">
        <div>
          <label class="block text-sm font-medium mb-2">Event Name</label>
          <input v-model="newEvent.name" class="input-field" required />
        </div>
        
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium mb-2">Date & Time</label>
            <input type="datetime-local" v-model="newEvent.date" class="input-field" required />
          </div>
          <div>
            <label class="block text-sm font-medium mb-2">Capacity</label>
            <input type="number" v-model="newEvent.capacity" class="input-field" placeholder="Leave empty for unlimited" />
          </div>
        </div>
        
        <div>
          <label class="block text-sm font-medium mb-2">Location</label>
          <input v-model="newEvent.location" class="input-field" required />
        </div>
        
        <div>
          <label class="block text-sm font-medium mb-2">Status</label>
          <select v-model="newEvent.status" class="input-field">
            <option value="upcoming">Upcoming</option>
            <option value="live">Live</option>
            <option value="completed">Completed</option>
            <option value="cancelled">Cancelled</option>
          </select>
        </div>
        
        <div class="flex gap-4">
          <label class="flex items-center gap-2">
            <input type="checkbox" v-model="newEvent.isTicketed" />
            <span class="text-sm">Ticketed Event</span>
          </label>
          <label class="flex items-center gap-2">
            <input type="checkbox" v-model="newEvent.hasSponsorship" />
            <span class="text-sm">Has Sponsorship</span>
          </label>
        </div>
        
        <div v-if="newEvent.isTicketed">
          <label class="block text-sm font-medium mb-2">Ticket Price ($)</label>
          <input type="number" v-model="newEvent.ticketPrice" class="input-field" />
        </div>
        
        <div class="flex gap-2">
          <Button type="button" variant="ghost" @click="showCreateModal = false">Cancel</Button>
          <Button type="submit" variant="primary">{{ editingEvent ? 'Update' : 'Create' }} Event</Button>
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

// Mock event data
const events = ref([
  {
    id: '1',
    name: 'Annual Gala 2026',
    date: 'August 15, 2026 at 6:00 PM',
    location: 'Atlanta Marriott Marquis',
    capacity: 300,
    isTicketed: true,
    ticketPrice: 75,
    hasSponsorship: true,
    status: 'upcoming',
    registrations: 187
  },
  {
    id: '2',
    name: 'Eid al-Adha Celebration',
    date: 'August 20, 2026 at 10:00 AM',
    location: 'School Campus',
    capacity: 500,
    isTicketed: false,
    ticketPrice: 0,
    hasSponsorship: false,
    status: 'upcoming',
    registrations: 312
  },
  {
    id: '3',
    name: 'Parent Orientation',
    date: 'August 25, 2026 at 5:30 PM',
    location: 'School Auditorium',
    capacity: 200,
    isTicketed: false,
    ticketPrice: 0,
    hasSponsorship: false,
    status: 'upcoming',
    registrations: 145
  },
  {
    id: '4',
    name: 'Ramadan Iftar 2026',
    date: 'March 15, 2026 at 6:30 PM',
    location: 'School Cafeteria',
    capacity: 400,
    isTicketed: false,
    ticketPrice: 0,
    hasSponsorship: true,
    status: 'completed',
    registrations: 389
  }
])

const filterStatus = ref('')
const showCreateModal = ref(false)
const editingEvent = ref<any>(null)

const newEvent = ref({
  name: '',
  date: '',
  location: '',
  capacity: 0,
  isTicketed: false,
  ticketPrice: 0,
  hasSponsorship: false,
  status: 'upcoming'
})

const filteredEvents = computed(() => {
  return events.value.filter(event => {
    return !filterStatus.value || event.status === filterStatus.value
  })
})

const upcomingEvents = computed(() => events.value.filter(e => e.status === 'upcoming').length)
const ticketedEvents = computed(() => events.value.filter(e => e.isTicketed).length)
const totalRegistrations = computed(() => events.value.reduce((sum, e) => sum + e.registrations, 0))
const totalRevenue = computed(() => {
  return events.value.reduce((sum, e) => {
    if (e.isTicketed) {
      return sum + (e.registrations * e.ticketPrice)
    }
    return sum
  }, 0)
})
const checkedIn = ref(0)

const getStatusVariant = (status: string) => {
  const variants: Record<string, string> = {
    upcoming: 'success',
    live: 'warning',
    completed: 'info',
    cancelled: 'danger'
  }
  return variants[status] || 'neutral'
}

const viewEvent = (id: string) => {
  navigateTo(`/events/${id}`)
}

const openCheckIn = (id: string) => {
  navigateTo(`/events/checkin/${id}`)
}

const editEvent = (id: string) => {
  const event = events.value.find(e => e.id === id)
  if (event) {
    editingEvent.value = event
    newEvent.value = { ...event }
    showCreateModal.value = true
  }
}

const deleteEvent = (id: string) => {
  if (confirm('Are you sure you want to delete this event?')) {
    events.value = events.value.filter(e => e.id !== id)
  }
}

const handleCreate = () => {
  if (editingEvent.value) {
    // Update existing event
    const index = events.value.findIndex(e => e.id === editingEvent.value.id)
    if (index !== -1) {
      events.value[index] = { ...newEvent.value }
    }
  } else {
    // Create new event
    const newId = Date.now().toString()
    const formattedDate = new Date(newEvent.value.date).toLocaleString('en-US', {
      weekday: undefined,
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: 'numeric',
      minute: '2-digit'
    })
    
    events.value.unshift({
      id: newId,
      name: newEvent.value.name,
      date: formattedDate,
      location: newEvent.value.location,
      capacity: newEvent.value.capacity,
      isTicketed: newEvent.value.isTicketed,
      ticketPrice: newEvent.value.ticketPrice || 0,
      hasSponsorship: newEvent.value.hasSponsorship,
      status: newEvent.value.status || 'upcoming',
      registrations: 0
    })
  }
  
  showCreateModal.value = false
  editingEvent.value = null
  
  // Reset form
  newEvent.value = {
    name: '',
    date: '',
    location: '',
    capacity: 0,
    isTicketed: false,
    ticketPrice: 0,
    hasSponsorship: false,
    status: 'upcoming'
  }
}
</script>
