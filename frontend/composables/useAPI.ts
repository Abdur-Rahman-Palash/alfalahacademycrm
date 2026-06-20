/**
 * API composable for making authenticated API requests
 */
import { useAuth } from './useAuth'

export function useAPI() {
  const { token, refreshToken, logout } = useAuth()
  const config = useRuntimeConfig()
  
  const fetchWithAuth = async <T = any>(
    url: string,
    options: RequestInit = {}
  ): Promise<T> => {
    let currentToken = token.value
    
    if (!currentToken && process.client) {
      currentToken = localStorage.getItem('access_token')
    }
    
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...(currentToken && { Authorization: `Bearer ${currentToken}` }),
      ...options.headers
    }
    
    try {
      const response = await fetch(`${config.public.apiBase}${url}`, {
        ...options,
        headers
      })
      
      if (response.status === 401) {
        // Try to refresh token
        const refreshed = await refreshToken()
        if (refreshed) {
          // Retry with new token
          const newToken = token.value || (process.client ? localStorage.getItem('access_token') : null)
          const retryResponse = await fetch(`${config.public.apiBase}${url}`, {
            ...options,
            headers: {
              ...headers,
              Authorization: `Bearer ${newToken}`
            }
          })
          
          if (!retryResponse.ok) {
            throw new Error('Request failed after token refresh')
          }
          
          return retryResponse.json()
        } else {
          // Logout if refresh fails
          await logout()
          throw new Error('Authentication failed')
        }
      }
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      return response.json()
    } catch (error) {
      console.error('API error:', error)
      throw error
    }
  }
  
  const get = <T = any>(url: string) => {
    return fetchWithAuth<T>(url, { method: 'GET' })
  }
  
  const post = <T = any>(url: string, data: any) => {
    return fetchWithAuth<T>(url, {
      method: 'POST',
      body: JSON.stringify(data)
    })
  }
  
  const put = <T = any>(url: string, data: any) => {
    return fetchWithAuth<T>(url, {
      method: 'PUT',
      body: JSON.stringify(data)
    })
  }
  
  const del = <T = any>(url: string) => {
    return fetchWithAuth<T>(url, { method: 'DELETE' })
  }
  
  return {
    fetch: fetchWithAuth,
    get,
    post,
    put,
    delete: del
  }
}
