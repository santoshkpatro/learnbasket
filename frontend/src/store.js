import { http } from './api/index'
import { reactive } from 'vue'

export const store = reactive({
  isAuthenticated: false,
  profile: null,
  access_token: '',
  setAuthentication(access_token) {
    this.access_token = access_token
    localStorage.setItem('access_token', JSON.stringify(access_token))
    http.defaults.headers.common['Authorization'] = `Bearer ${access_token}`
    this.isAuthenticated = true
  },
  removeAuthentication() {
    localStorage.removeItem('access_token')
    this.isAuthenticated = false
    location.reload()
  },
})
