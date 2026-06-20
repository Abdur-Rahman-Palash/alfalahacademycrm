<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 px-4">
    <div class="max-w-md w-full text-center">
      <div class="mx-auto h-16 w-16 rounded-full bg-red-100 flex items-center justify-center mb-6">
        <svg class="h-8 w-8 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M12 9v2m0 4h.01M5.07 19h13.86c1.54 0 2.5-1.67 1.73-3L13.73 4c-.77-1.33-2.69-1.33-3.46 0L3.34 16c-.77 1.33.19 3 1.73 3z" />
        </svg>
      </div>

      <h1 class="text-2xl font-semibold text-gray-900 mb-2">Access Denied</h1>
      <p class="text-gray-600 mb-8">
        আপনার এই পেজ দেখার পারমিশন নেই। যদি এটা ভুল মনে করেন, আপনার এডমিনের সাথে যোগাযোগ করুন।
      </p>

      <div class="flex flex-col sm:flex-row gap-3 justify-center">
        <NuxtLink
          to="/"
          class="px-5 py-2.5 rounded-lg bg-gray-900 text-white text-sm font-medium hover:bg-gray-800 transition"
        >
          Go to Dashboard
        </NuxtLink>
        <button
          @click="handleLogout"
          class="px-5 py-2.5 rounded-lg border border-gray-300 text-sm font-medium text-gray-700 hover:bg-gray-100 transition"
        >
          Sign out
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const { logout } = useAuth()

const handleLogout = async () => {
  await logout()
  navigateTo('/login')
}
</script>