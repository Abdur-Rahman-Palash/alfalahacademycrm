<template>
  <header class="bg-white border-b border-gray-200 shadow-sm">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">
        <!-- Logo -->
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <h1 class="text-2xl font-display font-bold text-primary-navy">
              Al Falah Academy
            </h1>
          </div>
        </div>

        <!-- Navigation -->
        <nav class="hidden md:flex items-center space-x-8">
          <a href="/" class="text-gray-700 hover:text-primary-navy font-medium transition-colors">
            Dashboard
          </a>
          <a href="/donors" class="text-gray-700 hover:text-primary-navy font-medium transition-colors">
            Donors
          </a>
          <a href="/campaigns" class="text-gray-700 hover:text-primary-navy font-medium transition-colors">
            Campaigns
          </a>
          <a href="/events" class="text-gray-700 hover:text-primary-navy font-medium transition-colors">
            Events
          </a>
          <a href="/portal/give" class="text-primary-gold hover:text-primary-navy font-medium transition-colors">
            Donate
          </a>
        </nav>

        <!-- Right side -->
        <div class="flex items-center space-x-4">
          <!-- Islamic Date -->
          <div class="hidden lg:block text-right">
            <p class="text-xs text-gray-500">{{ gregorianDate }}</p>
            <p class="text-xs font-arabic text-primary-emerald">{{ hijriDate }}</p>
          </div>

          <!-- User Menu -->
          <div class="relative">
            <button class="flex items-center space-x-2 text-gray-700 hover:text-primary-navy">
              <div class="w-8 h-8 rounded-full bg-primary-navy text-white flex items-center justify-center font-medium">
                A
              </div>
            </button>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
const gregorianDate = computed(() => {
  return new Date().toLocaleDateString('en-US', {
    weekday: 'short',
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
})

const hijriDate = computed(() => {
  // TODO: Implement actual Hijri conversion
  return '23 Dhul Hijjah 1447'
})
</script>
