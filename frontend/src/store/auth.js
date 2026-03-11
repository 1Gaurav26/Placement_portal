import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', {
    state: () => ({
        token: localStorage.getItem('token') || null,
        role: localStorage.getItem('role') || null,
    }),
    actions: {
        setAuth(token, role) {
            this.token = token
            this.role = role
            localStorage.setItem('token', token)
            localStorage.setItem('role', role)
            axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
        },
        logout() {
            this.token = null
            this.role = null
            localStorage.removeItem('token')
            localStorage.removeItem('role')
            delete axios.defaults.headers.common['Authorization']
        }
    }
})
