<template>
  <div class="row justify-content-center align-items-center" style="min-height: 80vh;">
    <div class="col-md-5 col-lg-4">
      <div class="card shadow-lg border-0" style="border-radius: 1rem; overflow: hidden;">
        <div class="bg-primary text-white text-center py-4" style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%) !important;">
          <h3 class="mb-0 fw-bold">Welcome Back</h3>
          <p class="mb-0 text-white-50">Sign in to your account</p>
        </div>
        <div class="card-body p-4 p-md-5">
          <div v-if="errorMsg" class="alert alert-danger border-0 shadow-sm">{{ errorMsg }}</div>
          
          <form @submit.prevent="handleLogin">
            <div class="mb-4">
              <label class="form-label text-muted fw-semibold small text-uppercase">Email address</label>
              <input type="email" class="form-control form-control-lg bg-light border-0 px-4" v-model="email" required placeholder="name@example.com" style="border-radius: 8px;">
            </div>
            <div class="mb-5">
              <label class="form-label text-muted fw-semibold small text-uppercase">Password</label>
              <input type="password" class="form-control form-control-lg bg-light border-0 px-4" v-model="password" required placeholder="••••••••" style="border-radius: 8px;">
            </div>
            <button type="submit" class="btn btn-primary btn-lg w-100 shadow-sm fw-bold" :disabled="loading" style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); border: none; border-radius: 8px;">
              {{ loading ? 'Signing in...' : 'Sign In' }}
            </button>
          </form>
          
          <div class="text-center mt-4">
            <p class="text-muted mb-2">Don't have an account?</p>
            <router-link to="/register/student" class="btn btn-outline-primary btn-sm me-2 fw-semibold">Register as Student</router-link>
            <router-link to="/register/company" class="btn btn-outline-success btn-sm fw-semibold">Register as Company</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../store/auth'

const email = ref('')
const password = ref('')
const errorMsg = ref('')
const loading = ref(false)
const router = useRouter()
const authStore = useAuthStore()

const handleLogin = async () => {
  loading.value = true
  errorMsg.value = ''
  try {
    const res = await axios.post('/auth/login', { email: email.value, password: password.value })
    authStore.setAuth(res.data.access_token, res.data.role)
    if (res.data.role === 'admin') router.push('/admin')
    else if (res.data.role === 'company') router.push('/company')
    else if (res.data.role === 'student') router.push('/student')
  } catch (err) {
    errorMsg.value = err.response?.data?.msg || 'Login failed'
  } finally {
    loading.value = false
  }
}
</script>
