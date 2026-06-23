/**
 * Authentication composable for managing user auth state
 */
import { ref, computed } from 'vue'

interface User {
  id: string
  email: string
  role: string
  name?: string
}

interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
}

const authState = ref<AuthState>({
  user: null,
  token: null,
  isAuthenticated: false
})

export function useAuth() {
  const register = async (email: string, password: string, name?: string) => {
    try {
      const config = useRuntimeConfig()
      console.log('Attempting registration to:', `${config.public.apiBase}/auth/register`)
      console.log('Registration data:', { email, name })
      
      const response = await $fetch<any>(
        `${config.public.apiBase}/auth/register`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: {
            email,
            password,
            role: 'read_only',
            permissions: {},
            is_active: true
          }
        }
      )
      
      console.log('Registration successful:', response)
      
      // After successful registration, automatically login
      const loginResult = await login(email, password)
      return loginResult
    } catch (error: any) {
      console.error('Registration error:', error)
      console.error('Error details:', error.data || error.message)
      console.error('Error status:', error.status || error.statusCode)
      return { 
        success: false, 
        error: error.data?.detail || error.message || 'Registration failed' 
      }
    }
  }

  const login = async (email: string, password: string) => {
    try {
      const config = useRuntimeConfig()

      // FastAPI's OAuth2PasswordRequestForm expects
      // application/x-www-form-urlencoded data, not JSON
      const formData = new URLSearchParams()
      formData.append('username', email)
      formData.append('password', password)

      const response = await $fetch<{ access_token: string; refresh_token: string }>(
        `${config.public.apiBase}/auth/login`,
        {
          method: 'POST',
          body: formData,
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        }
      )
      
      // Store tokens
      if (process.client) {
        localStorage.setItem('access_token', response.access_token)
        localStorage.setItem('refresh_token', response.refresh_token)
      }
      
      authState.value.token = response.access_token
      authState.value.isAuthenticated = true
      
      // Fetch user info
      await fetchCurrentUser()
      
      return { success: true }
    } catch (error: any) {
      console.error('Login error:', error)
      return { 
        success: false, 
        error: error.data?.detail || error.message || 'Login failed' 
      }
    }
  }
  
  const logout = async () => {
    try {
      // TEMPORARILY COMMENTED OUT - BACKEND ENDPOINT NOT IMPLEMENTED
      // const config = useRuntimeConfig()
      // await $fetch(`${config.public.apiBase}/auth/logout`, {
      //   method: 'POST'
      // })
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      // Clear local state
      if (process.client) {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
      }
      
      authState.value = {
        user: null,
        token: null,
        isAuthenticated: false
      }
    }
  }
  
  const fetchCurrentUser = async () => {
    try {
      const config = useRuntimeConfig()
      const token = process.client ? localStorage.getItem('access_token') : null
      
      if (!token) {
        return
      }
      
      const user = await $fetch<User>(`${config.public.apiBase}/auth/me`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
      
      authState.value.user = user
      authState.value.isAuthenticated = true
    } catch (error) {
      console.error('Fetch user error:', error)
      authState.value.isAuthenticated = false
    }
  }
  
  const refreshToken = async () => {
    try {
      const config = useRuntimeConfig()
      const refreshToken = process.client ? localStorage.getItem('refresh_token') : null
      
      if (!refreshToken) {
        return false
      }
      
      const response = await $fetch<{ access_token: string; refresh_token: string }>(
        `${config.public.apiBase}/auth/refresh`,
        {
          method: 'POST',
          headers: {
            Authorization: `Bearer ${refreshToken}`
          }
        }
      )
      
      if (process.client) {
        localStorage.setItem('access_token', response.access_token)
        localStorage.setItem('refresh_token', response.refresh_token)
      }
      
      authState.value.token = response.access_token
      return true
    } catch (error) {
      console.error('Refresh token error:', error)
      return false
    }
  }
  
  const hasPermission = (requiredRole: string) => {
    if (!authState.value.user) {
      return false
    }
    
    const roleHierarchy = {
      'super_admin': 5,
      'admin': 4,
      'development': 3,
      'events': 2,
      'read_only': 1
    }
    
    const userLevel = roleHierarchy[authState.value.user.role as keyof typeof roleHierarchy] || 0
    const requiredLevel = roleHierarchy[requiredRole as keyof typeof roleHierarchy] || 0
    
    return userLevel >= requiredLevel
  }
  
  // Initialize auth state on mount
 const initializeAuth = async () => {
    if (process.client) {
      const token = localStorage.getItem('access_token')
      if (token) {
        authState.value.token = token
        await fetchCurrentUser()
      }
    }
  }
  
  return {
    user: computed(() => authState.value.user),
    token: computed(() => authState.value.token),
    isAuthenticated: computed(() => authState.value.isAuthenticated),
    register,
    login,
    logout,
    fetchCurrentUser,
    refreshToken,
    hasPermission,
    initializeAuth
  }
}