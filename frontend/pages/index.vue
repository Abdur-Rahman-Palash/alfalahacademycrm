<template>
  <div class="space-y-8">
    <!-- Welcome Section -->
    <div class="relative overflow-hidden rounded-2xl bg-gradient-to-r from-primary-navy via-primary-blue to-primary-gold p-8 text-white shadow-2xl fade-in-up">
      <div class="absolute top-0 right-0 w-64 h-64 bg-white/10 rounded-full -translate-y-1/2 translate-x-1/2 blur-3xl" />
      <div class="absolute bottom-0 left-0 w-48 h-48 bg-primary-gold/20 rounded-full translate-y-1/2 -translate-x-1/2 blur-2xl" />
      <div class="relative z-10">
        <h1 class="text-4xl font-display font-bold mb-2">Welcome to Al Falah Academy CRM</h1>
        <p class="text-lg opacity-90 mb-6">Manage your donors, campaigns, events, and scholarships all in one place</p>
        <div class="flex gap-4">
          <div class="bg-white/20 backdrop-blur-sm rounded-lg px-4 py-2">
            <p class="text-2xl font-bold">$127,450</p>
            <p class="text-xs opacity-80">Raised this month</p>
          </div>
          <div class="bg-white/20 backdrop-blur-sm rounded-lg px-4 py-2">
            <p class="text-2xl font-bold">847</p>
            <p class="text-xs opacity-80">Active donors</p>
          </div>
          <div class="bg-white/20 backdrop-blur-sm rounded-lg px-4 py-2">
            <p class="text-2xl font-bold">12</p>
            <p class="text-xs opacity-80">Active campaigns</p>
          </div>
        </div>
      </div>
    </div>

    <!-- KPI Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <div v-for="(kpi, index) in kpiData" :key="kpi.title" class="group relative overflow-hidden rounded-2xl bg-white shadow-lg hover:shadow-2xl transition-all duration-300 hover:-translate-y-1 scale-in" :style="{ animationDelay: `${index * 0.1}s` }">
        <div class="absolute inset-0 bg-gradient-to-br from-transparent to-gray-50 opacity-0 group-hover:opacity-100 transition-opacity" />
        <div class="relative p-6">
          <div class="flex items-start justify-between mb-4">
            <div :class="kpi.iconBg" class="w-14 h-14 rounded-xl flex items-center justify-center shadow-lg group-hover:scale-110 transition-transform">
              <span v-html="kpi.icon" class="w-7 h-7" />
            </div>
            <div class="flex items-center gap-1 px-2 py-1 rounded-full" :class="kpi.trendBg">
              <svg class="w-4 h-4" :class="kpi.trendArrowClass" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
              </svg>
              <span class="text-xs font-medium" :class="kpi.trendTextClass">{{ kpi.trendValue }}</span>
            </div>
          </div>
          <p class="text-sm text-gray-500 mb-1">{{ kpi.title }}</p>
          <p class="text-3xl font-display font-bold text-primary-navy">{{ kpi.value }}</p>
          <p :class="kpi.trendClass" class="text-sm mt-2">{{ kpi.trend }}</p>
        </div>
      </div>
    </div>
    <!-- Charts and Recent Activity -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Donation Chart -->
      <div class="lg:col-span-2 rounded-2xl bg-white shadow-lg hover:shadow-xl transition-shadow fade-in-up" style="animation-delay: 0.5s">
        <div class="p-6 border-b border-gray-100">
          <div class="flex items-center justify-between">
            <h3 class="text-xl font-display font-bold text-primary-navy">Donation Trends</h3>
            <div class="flex gap-2">
              <button class="px-3 py-1 text-sm rounded-full bg-primary-navy text-white">Monthly</button>
              <button class="px-3 py-1 text-sm rounded-full bg-gray-100 text-gray-600 hover:bg-gray-200">Yearly</button>
            </div>
          </div>
        </div>
        <div class="p-6">
          <DonationChart />
        </div>
      </div>

      <!-- Recent Donations -->
      <div class="rounded-2xl bg-white shadow-lg hover:shadow-xl transition-shadow fade-in-up" style="animation-delay: 0.6s">
        <div class="p-6 border-b border-gray-100">
          <div class="flex items-center justify-between">
            <h3 class="text-xl font-display font-bold text-primary-navy">Recent Donations</h3>
            <button class="text-primary-gold hover:text-primary-gold/80 text-sm font-medium">View All</button>
          </div>
        </div>
        <div class="p-4 space-y-3">
          <div v-for="(donation, index) in recentDonations" :key="donation.id" class="flex items-center gap-4 p-4 rounded-xl bg-gradient-to-r from-gray-50 to-white hover:from-primary-gold/5 hover:to-white transition-all cursor-pointer group" style="animation-delay: `${0.7 + index * 0.1}s`">
            <div class="w-12 h-12 rounded-full bg-gradient-to-br from-primary-navy to-primary-blue flex items-center justify-center text-white font-bold shadow-lg group-hover:scale-110 transition-transform">
              {{ donation.initials }}
            </div>
            <div class="flex-1 min-w-0">
              <p class="text-sm font-semibold text-gray-900 truncate group-hover:text-primary-navy transition-colors">{{ donation.name }}</p>
              <p class="text-xs text-gray-500">{{ donation.date }}</p>
            </div>
            <div class="text-right">
              <p class="text-lg font-bold text-primary-emerald">${{ donation.amount }}</p>
              <p class="text-xs text-gray-400">USD</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Active Campaigns & Upcoming Events -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Active Campaigns -->
      <div class="rounded-2xl bg-white shadow-lg hover:shadow-xl transition-shadow fade-in-up" style="animation-delay: 0.8s">
        <div class="p-6 border-b border-gray-100">
          <div class="flex items-center justify-between">
            <h3 class="text-xl font-display font-bold text-primary-navy">Active Campaigns</h3>
            <button class="text-primary-gold hover:text-primary-gold/80 text-sm font-medium">View All</button>
          </div>
        </div>
        <div class="p-4 space-y-4">
          <div v-for="(campaign, index) in activeCampaigns" :key="campaign.id" class="group p-4 rounded-xl bg-gradient-to-br from-gray-50 to-white hover:from-primary-navy/5 hover:to-primary-gold/5 transition-all cursor-pointer">
            <div class="flex items-center justify-between mb-3">
              <span class="text-sm font-semibold text-primary-navy group-hover:text-primary-gold transition-colors">{{ campaign.name }}</span>
              <span class="text-sm font-medium text-gray-600">${{ campaign.raised }} / ${{ campaign.goal }}</span>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
              <div 
                class="bg-gradient-to-r from-primary-gold to-primary-emerald h-3 rounded-full transition-all duration-700 ease-out"
                :style="{ width: campaign.progress + '%' }"
              />
            </div>
            <div class="flex items-center justify-between mt-2">
              <span class="text-xs text-gray-500">{{ campaign.progress }}% complete</span>
              <span class="text-xs font-medium text-primary-emerald">{{ campaign.progress >= 75 ? 'Almost there!' : campaign.progress >= 50 ? 'Halfway!' : 'Keep going!' }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Upcoming Events -->
      <div class="rounded-2xl bg-white shadow-lg hover:shadow-xl transition-shadow fade-in-up" style="animation-delay: 0.9s">
        <div class="p-6 border-b border-gray-100">
          <div class="flex items-center justify-between">
            <h3 class="text-xl font-display font-bold text-primary-navy">Upcoming Events</h3>
            <button class="text-primary-gold hover:text-primary-gold/80 text-sm font-medium">View All</button>
          </div>
        </div>
        <div class="p-4 space-y-3">
          <div v-for="(event, index) in upcomingEvents" :key="event.id" class="flex items-center gap-4 p-4 rounded-xl bg-gradient-to-r from-primary-gray to-white hover:from-primary-navy/10 hover:to-primary-gold/10 transition-all cursor-pointer group">
            <div class="w-16 h-16 rounded-xl bg-gradient-to-br from-primary-navy to-primary-blue flex items-center justify-center text-white shadow-lg group-hover:scale-110 transition-transform">
              <div class="text-center">
                <p class="text-xl font-display font-bold">{{ event.day }}</p>
                <p class="text-xs opacity-90">{{ event.month }}</p>
              </div>
            </div>
            <div class="flex-1">
              <p class="text-sm font-semibold text-gray-900 group-hover:text-primary-navy transition-colors">{{ event.name }}</p>
              <p class="text-xs text-gray-500">{{ event.location }}</p>
            </div>
            <div class="px-3 py-1 rounded-full bg-primary-emerald/10 text-primary-emerald text-xs font-medium">
              {{ event.status }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- GaSSO Pipeline -->
    <div class="rounded-2xl bg-gradient-to-r from-primary-navy to-primary-blue shadow-lg hover:shadow-xl transition-shadow fade-in-up" style="animation-delay: 1s">
      <div class="p-6 border-b border-white/10">
        <div class="flex items-center justify-between">
          <h3 class="text-xl font-display font-bold text-white">GaSSO Scholarship Pipeline</h3>
          <div class="flex items-center gap-2 px-3 py-1 rounded-full bg-white/20">
            <div class="w-2 h-2 rounded-full bg-primary-emerald animate-pulse" />
            <span class="text-xs font-medium text-white">Live</span>
          </div>
        </div>
      </div>
      <div class="p-6">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div v-for="(stage, index) in gassoPipeline" :key="stage.name" class="group relative overflow-hidden rounded-xl bg-white/10 backdrop-blur-sm p-6 hover:bg-white/20 transition-all cursor-pointer" style="animation-delay: `${1.1 + index * 0.1}s`">
            <div class="absolute inset-0 bg-gradient-to-br from-transparent to-white/5 opacity-0 group-hover:opacity-100 transition-opacity" />
            <div class="relative">
              <p class="text-4xl font-display font-bold text-white mb-2">{{ stage.count }}</p>
              <p class="text-sm text-white/80 mb-1">{{ stage.name }}</p>
              <p class="text-lg font-bold text-primary-gold">${{ stage.total }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="rounded-2xl bg-white shadow-lg hover:shadow-xl transition-shadow fade-in-up" style="animation-delay: 1.2s">
      <div class="p-6 border-b border-gray-100">
        <h3 class="text-xl font-display font-bold text-primary-navy">Quick Actions</h3>
      </div>
      <div class="p-6">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <button @click="handleAction('donor')" class="group relative overflow-hidden rounded-xl bg-gradient-to-br from-primary-navy to-primary-blue p-6 text-white shadow-lg hover:shadow-xl hover:-translate-y-1 transition-all">
            <div class="absolute inset-0 bg-gradient-to-br from-white/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
            <div class="relative">
              <div class="w-12 h-12 mx-auto mb-3 rounded-xl bg-white/20 flex items-center justify-center group-hover:scale-110 transition-transform">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
                </svg>
              </div>
              <p class="text-sm font-semibold text-center">Add Donor</p>
            </div>
          </button>
          <button @click="handleAction('donation')" class="group relative overflow-hidden rounded-xl bg-gradient-to-br from-primary-emerald to-primary-teal p-6 text-white shadow-lg hover:shadow-xl hover:-translate-y-1 transition-all">
            <div class="absolute inset-0 bg-gradient-to-br from-white/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
            <div class="relative">
              <div class="w-12 h-12 mx-auto mb-3 rounded-xl bg-white/20 flex items-center justify-center group-hover:scale-110 transition-transform">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <p class="text-sm font-semibold text-center">Add Donation</p>
            </div>
          </button>
          <button @click="handleAction('event')" class="group relative overflow-hidden rounded-xl bg-gradient-to-br from-primary-gold to-primary-orange p-6 text-white shadow-lg hover:shadow-xl hover:-translate-y-1 transition-all">
            <div class="absolute inset-0 bg-gradient-to-br from-white/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
            <div class="relative">
              <div class="w-12 h-12 mx-auto mb-3 rounded-xl bg-white/20 flex items-center justify-center group-hover:scale-110 transition-transform">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </div>
              <p class="text-sm font-semibold text-center">Create Event</p>
            </div>
          </button>
          <button @click="handleAction('campaign')" class="group relative overflow-hidden rounded-xl bg-gradient-to-br from-purple-600 to-pink-500 p-6 text-white shadow-lg hover:shadow-xl hover:-translate-y-1 transition-all">
            <div class="absolute inset-0 bg-gradient-to-br from-white/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
            <div class="relative">
              <div class="w-12 h-12 mx-auto mb-3 rounded-xl bg-white/20 flex items-center justify-center group-hover:scale-110 transition-transform">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <p class="text-sm font-semibold text-center">New Campaign</p>
            </div>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// TEMPORARILY DISABLED AUTH MIDDLEWARE
// definePageMeta({
//   middleware: 'auth',
//   requiredRole: 'read_only'
// })

import Card from '~/components/ui/Card.vue'
import Button from '~/components/ui/Button.vue'
import Badge from '~/components/ui/Badge.vue'
import DonationChart from '~/components/ui/DonationChart.vue'

// KPI Data
const kpiData = [
  {
    title: 'Total Raised (Month)',
    value: '$127,450',
    trend: '+12.5% from last month',
    trendClass: 'text-primary-emerald',
    trendValue: '+12.5%',
    trendBg: 'bg-primary-emerald/10',
    trendTextClass: 'text-primary-emerald',
    trendArrowClass: 'text-primary-emerald',
    icon: '<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>',
    iconBg: 'bg-gradient-to-br from-primary-gold to-primary-orange'
  },
  {
    title: 'Active Donors',
    value: '847',
    trend: '+23 new this month',
    trendClass: 'text-primary-emerald',
    trendValue: '+23',
    trendBg: 'bg-primary-emerald/10',
    trendTextClass: 'text-primary-emerald',
    trendArrowClass: 'text-primary-emerald',
    icon: '<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" /></svg>',
    iconBg: 'bg-gradient-to-br from-primary-emerald to-primary-teal'
  },
  {
    title: 'Recurring Gifts',
    value: '$45,200',
    trend: 'Monthly recurring',
    trendClass: 'text-primary-navy',
    trendValue: 'Stable',
    trendBg: 'bg-primary-navy/10',
    trendTextClass: 'text-primary-navy',
    trendArrowClass: 'text-primary-navy',
    icon: '<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" /></svg>',
    iconBg: 'bg-gradient-to-br from-primary-blue to-primary-indigo'
  },
  {
    title: 'Event Registrations',
    value: '312',
    trend: 'Next event: 45 days',
    trendClass: 'text-primary-navy',
    trendValue: 'Active',
    trendBg: 'bg-primary-gold/10',
    trendTextClass: 'text-primary-gold',
    trendArrowClass: 'text-primary-gold',
    icon: '<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>',
    iconBg: 'bg-gradient-to-br from-primary-purple to-primary-pink'
  }
]

// Recent Donations
const recentDonations = [
  { id: 1, name: 'Ahmed Family', initials: 'AF', date: 'Today', amount: '500' },
  { id: 2, name: 'Mohammed Corp', initials: 'MC', date: 'Yesterday', amount: '1,000' },
  { id: 3, name: 'Sarah Khan', initials: 'SK', date: '2 days ago', amount: '250' },
  { id: 4, name: 'Omar Foundation', initials: 'OF', date: '3 days ago', amount: '5,000' },
]

// Active Campaigns
const activeCampaigns = [
  { id: 1, name: 'Ramadan 2026', raised: '85,000', goal: '100,000', progress: 85 },
  { id: 2, name: 'Annual Fund', raised: '42,500', goal: '75,000', progress: 57 },
  { id: 3, name: 'Building Expansion', raised: '150,000', goal: '500,000', progress: 30 },
]

// Upcoming Events
const upcomingEvents = [
  { id: 1, name: 'Annual Gala', day: '15', month: 'Aug', location: 'Atlanta Marriott', status: 'upcoming' },
  { id: 2, name: 'Eid Celebration', day: '20', month: 'Aug', location: 'School Campus', status: 'upcoming' },
  { id: 3, name: 'Parent Meeting', day: '25', month: 'Aug', location: 'School Auditorium', status: 'upcoming' },
]

// GaSSO Pipeline
const gassoPipeline = [
  { name: 'Pledged', count: 45, total: '225,000' },
  { name: 'Approved', count: 38, total: '190,000' },
  { name: 'Partially Funded', count: 12, total: '60,000' },
  { name: 'Fully Funded', count: 28, total: '140,000' },
]

const handleAction = (action: string) => {
  switch (action) {
    case 'donor':
      navigateTo('/donors')
      break
    case 'donation':
      navigateTo('/donations')
      break
    case 'event':
      navigateTo('/events')
      break
    case 'campaign':
      navigateTo('/campaigns')
      break
    default:
      console.log('Unknown action:', action)
  }
}

// GSAP Animation on mount
onMounted(() => {
  // TODO: Implement GSAP animations
  console.log('Dashboard mounted - animations to be implemented')
})
</script>