<template>
  <div class="min-h-screen bg-primary-ivory flex flex-col">
    <!-- Header -->
    <Header />
    
    <!-- Main Content -->
    <div class="flex flex-1">
      <!-- Sidebar -->
      <Sidebar />
      
      <!-- Main Content Area -->
      <div class="flex-1 flex flex-col overflow-hidden">
        <!-- Page Header -->
        <header class="bg-white border-b border-gray-200 px-6 py-4">
          <div class="flex items-center justify-between">
            <div>
              <h2 class="text-xl font-display text-primary-navy">{{ pageTitle }}</h2>
              <p class="text-sm text-gray-500">{{ pageSubtitle }}</p>
            </div>
            
            <div class="flex items-center gap-4">
              <!-- Islamic Date -->
              <div class="text-right">
                <p class="text-sm font-medium text-primary-charcoal">{{ gregorianDate }}</p>
                <p class="text-sm font-arabic text-primary-emerald">{{ hijriDate }}</p>
              </div>
              
              <!-- Quick Actions -->
              <Button variant="primary" @click="handleQuickAction">
                + Quick Action
              </Button>
            </div>
          </div>
        </header>
        
        <!-- Page Content -->
        <main class="flex-1 overflow-y-auto p-6">
          <slot />
        </main>
      </div>
    </div>
    
    <!-- Footer -->
    <Footer />
  </div>
</template>

<script setup lang="ts">
import Header from '~/components/layout/Header.vue'
import Sidebar from '~/components/layout/Sidebar.vue'
import Footer from '~/components/layout/Footer.vue'

const route = useRoute()

const pageTitle = computed(() => {
  const titles: Record<string, string> = {
    '/': 'Dashboard',
    '/donors': 'Donors',
    '/donations': 'Donations',
    '/campaigns': 'Campaigns',
    '/events': 'Events',
    '/scholarship': 'GaSSO Scholarships',
    '/communications': 'Communications',
    '/reports': 'Reports'
  }
  return titles[route.path] || 'Dashboard'
})

const pageSubtitle = computed(() => {
  const subtitles: Record<string, string> = {
    '/': 'Overview and analytics',
    '/donors': 'Manage constituents',
    '/donations': 'Track donations',
    '/campaigns': 'Fundraising campaigns',
    '/events': 'Event management',
    '/scholarship': 'Scholarship tracking',
    '/communications': 'Email marketing',
    '/reports': 'Data exports'
  }
  return subtitles[route.path] || ''
})

// Islamic date calculation
const gregorianDate = computed(() => {
  return new Date().toLocaleDateString('en-US', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
})

const hijriDate = computed(() => {
  // TODO: Implement actual Hijri conversion
  return '23 Dhul Hijjah 1447'
})

const handleQuickAction = () => {
  // TODO: Implement quick action modal
  console.log('Quick action clicked')
}
</script>
