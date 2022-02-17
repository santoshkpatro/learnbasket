import axios from 'axios'
const access_token_string = localStorage.getItem('access_token')
const access_token = JSON.parse(access_token_string)

export const http = axios.create({
  baseURL: 'http://127.0.0.1:8000/v1',
})

const authHttp = axios.create({
  baseURL: 'http://127.0.0.1:8000/v1',
  headers: {
    Authorization: `Bearer ${access_token}`,
  },
})

export const authStatus = (access_token = None) =>
  http.get('/auth/status/', {
    headers: {
      Authorization: `Bearer ${access_token}`,
    },
  })

export const login = (data) => http.post('/auth/login/', data)
export const register = (data) => http.post('/auth/register/', data)
export const authProfile = () => http.get('/auth/profile/')
export const verifyEmail = (verify_token) =>
  http.get('/auth/verify/', {
    params: {
      verify_token: verify_token,
    },
  })
export const googleCallback = (code, mode) =>
  http.get('/auth/oauth/google/callback', {
    params: {
      code,
      mode,
    },
  })
