export default defineNuxtRouteMiddleware((to) => {
  const { isAuthenticated, hasPermission } = useAuth()

  // Login/signup করা না থাকলে login page এ পাঠিয়ে দিন
  // TEMPORARILY COMMENTED OUT TO ALLOW DIRECT ACCESS
  // if (!isAuthenticated.value) {
  //   return navigateTo('/login')
  // }

  // page এ requiredRole সেট করা থাকলে, role check করুন
  // TEMPORARILY COMMENTED OUT TO ALLOW DIRECT ACCESS
  // const requiredRole = to.meta.requiredRole as string | undefined
  // if (requiredRole && !hasPermission(requiredRole)) {
  //   return navigateTo('/unauthorized')
  // }
})