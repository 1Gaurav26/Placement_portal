<template>
  <div class="row justify-content-center align-items-center" style="min-height: 80vh;">
    <div class="col-md-8 col-lg-6">
      <div class="card shadow-lg border-0" style="border-radius: 1rem; overflow: hidden;">
        <div class="bg-primary text-white text-center py-4" style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%) !important;">
          <h3 class="mb-0 fw-bold">Student Registration</h3>
          <p class="mb-0 text-white-50">Join the Placement Portal</p>
        </div>
        <div class="card-body p-4 p-md-5">
          <div v-if="errorMsg" class="alert alert-danger border-0 shadow-sm">{{ errorMsg }}</div>
          <div v-if="successMsg" class="alert alert-success border-0 shadow-sm">{{ successMsg }}</div>
          
          <form @submit.prevent="handleRegister">
             <div class="row">
               <div class="col-md-6 mb-4">
                 <label class="form-label text-muted fw-semibold small text-uppercase">First Name</label>
                 <input type="text" class="form-control form-control-lg bg-light border-0 px-3" v-model="form.first_name" required style="border-radius: 8px;">
               </div>
               <div class="col-md-6 mb-4">
                 <label class="form-label text-muted fw-semibold small text-uppercase">Last Name</label>
                 <input type="text" class="form-control form-control-lg bg-light border-0 px-3" v-model="form.last_name" required style="border-radius: 8px;">
               </div>
             </div>
             <div class="mb-4">
               <label class="form-label text-muted fw-semibold small text-uppercase">Email address</label>
               <input type="email" class="form-control form-control-lg bg-light border-0 px-4" v-model="form.email" required style="border-radius: 8px;">
             </div>
             <div class="mb-4">
               <label class="form-label text-muted fw-semibold small text-uppercase">Password</label>
               <input type="password" class="form-control form-control-lg bg-light border-0 px-4" v-model="form.password" required style="border-radius: 8px;">
             </div>
             <div class="row">
               <div class="col-md-4 mb-4">
                 <label class="form-label text-muted fw-semibold small text-uppercase">Branch</label>
                 <input type="text" class="form-control form-control-lg bg-light border-0 px-3" v-model="form.branch" required placeholder="e.g. CSE" style="border-radius: 8px;">
               </div>
               <div class="col-md-4 mb-4">
                 <label class="form-label text-muted fw-semibold small text-uppercase">CGPA</label>
                 <input type="number" step="0.01" class="form-control form-control-lg bg-light border-0 px-3" v-model="form.cgpa" required style="border-radius: 8px;">
               </div>
               <div class="col-md-4 mb-5">
                 <label class="form-label text-muted fw-semibold small text-uppercase">Grad Year</label>
                 <input type="number" class="form-control form-control-lg bg-light border-0 px-3" v-model="form.graduation_year" required style="border-radius: 8px;">
               </div>
             </div>
             <button type="submit" class="btn btn-primary btn-lg w-100 shadow-sm fw-bold" :disabled="loading" style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); border: none; border-radius: 8px;">
               {{ loading ? 'Registering...' : 'Complete Registration' }}
             </button>
          </form>
          
          <div class="text-center mt-4">
            <p class="text-muted mb-0">Already have an account? <router-link to="/login" class="text-primary fw-semibold text-decoration-none">Sign In</router-link></p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const form = reactive({
  first_name: '', last_name: '', email: '', password: '', branch: '', cgpa: '', graduation_year: 2026
})
const errorMsg = ref('')
const successMsg = ref('')
const loading = ref(false)
const router = useRouter()

const handleRegister = async () => {
  loading.value = true
  errorMsg.value = ''
  successMsg.value = ''
  try {
    await axios.post('/auth/register/student', form)
    successMsg.value = 'Registration successful! Redirecting to login...'
    setTimeout(() => router.push('/login'), 2000)
  } catch (err) {
    errorMsg.value = err.response?.data?.msg || 'Registration failed'
  } finally {
    loading.value = false
  }
}
</script>
