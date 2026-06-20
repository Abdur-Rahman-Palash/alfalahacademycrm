<template>
  <aside :class="sidebarClasses">
    <!-- Logo -->
    <div class="p-6 border-b border-gray-200">
      <h1 class="font-display text-xl text-primary-navy">Al Falah Academy</h1>
      <p class="text-sm text-gray-500 mt-1">CRM System</p>
    </div>
    
    <!-- Navigation -->
    <nav class="flex-1 p-4 overflow-y-auto">
      <ul class="space-y-1">
        <li v-for="item in navigation" :key="item.name">
          <NuxtLink
            :to="item.href"
            class="flex items-center gap-3 px-4 py-3 rounded-lg transition-colors"
            :class="isActive(item.href) ? 'bg-primary-gold text-white' : 'text-gray-700 hover:bg-primary-gray'"
          >
            <span v-html="item.icon" />
            <span>{{ item.name }}</span>
          </NuxtLink>
        </li>
      </ul>
    </nav>
    
    <!-- User Info -->
    <div class="p-4 border-t border-gray-200">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-full bg-primary-navy flex items-center justify-center text-white font-medium">
          {{ userInitials }}
        </div>
        <div class="flex-1 min-w-0">
          <p class="text-sm font-medium text-gray-900 truncate">{{ userName }}</p>
          <p class="text-xs text-gray-500 truncate">{{ userEmail }}</p>
        </div>
      </div>
    </div>
  </aside>
</template>

<script setup lang="ts">
interface NavItem {
  name: string
  href: string
  icon: string
}

const navigation: NavItem[] = [
  { name: 'Dashboard', href: '/', icon: '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" /></svg>' },
  { name: 'Donors', href: '/donors', icon: '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" /></svg>' },
  { name: 'Donations', href: '/donations', icon: '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>' },
  { name: 'Campaigns', href: '/campaigns', icon: '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 3.055A9.001 9.001 0 1020.945 13H11V3.055z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.488 9H15V3.512A9.025 9.025 0 0120.488 9z" /></svg>' },
  { name: 'Events', href: '/events', icon: '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>' },
  { name: 'Scholarships', href: '/scholarship', icon: '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l9-5-9-5-9 5 9 5z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l9-5-9-5-9 5 9 5zm0 0l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14zm-4 6v-7.5l4-2.222" /></svg>' },
  { name: 'Communications', href: '/communications', icon: '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" /></svg>' },
  { name: 'Reports', href: '/reports', icon: '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>' },
]

const route = useRoute()

const isActive = (href: string) => {
  if (href === '/') {
    return route.path === '/'
  }
  return route.path.startsWith(href)
}

// Mock user data - replace with actual auth
const userName = ref('Admin User')
const userEmail = ref('admin@alfalahacademy.com')

const userInitials = computed(() => {
  const names = userName.value.split(' ')
  return names.map(n => n[0]).join('').toUpperCase()
})

const isCollapsed = ref(false)

const sidebarClasses = computed(() => {
  const base = 'flex flex-col h-full bg-white border-r border-gray-200 transition-all duration-300'
  const width = isCollapsed.value ? 'w-20' : 'w-64'
  return [base, width].join(' ')
})
</script>
