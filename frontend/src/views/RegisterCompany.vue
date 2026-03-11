<template>
  <div class="row justify-content-center align-items-center" style="min-height: 80vh;">
    <div class="col-md-8 col-lg-6">
      <div class="card shadow-lg border-0" style="border-radius: 1rem; overflow: hidden;">
        <div class="bg-success text-white text-center py-4" style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%) !important;">
          <h3 class="mb-0 fw-bold">Company Registration</h3>
          <p class="mb-0 text-white-50">Partner with our Institute</p>
        </div>
        <div class="card-body p-4 p-md-5">
          <div v-if="errorMsg" class="alert alert-danger border-0 shadow-sm">{{ errorMsg }}</div>
          <div v-if="successMsg" class="alert alert-success border-0 shadow-sm">{{ successMsg }}</div>
          
          <form @submit.prevent="handleRegister">
             <div class="mb-4">
               <label class="form-label text-muted fw-semibold small text-uppercase">Company Name</label>
               <input type="text" class="form-control form-control-lg bg-light border-0 px-4" v-model="form.company_name" required style="border-radius: 8px;">
             </div>
             <div class="mb-4">
               <label class="form-label text-muted fw-semibold small text-uppercase">HR Contact Name</label>
               <input type="text" class="form-control form-control-lg bg-light border-0 px-4" v-model="form.hr_contact" required style="border-radius: 8px;">
             </div>
             <div class="mb-4">
               <label class="form-label text-muted fw-semibold small text-uppercase">Company Website</label>
               <input type="url" class="form-control form-control-lg bg-light border-0 px-4" v-model="form.website" placeholder="https://" style="border-radius: 8px;">
             </div>
             <div class="mb-4">
               <label class="form-label text-muted fw-semibold small text-uppercase">Email address (for login)</label>
               <input type="email" class="form-control form-control-lg bg-light border-0 px-4" v-model="form.email" required style="border-radius: 8px;">
             </div>
             <div class="mb-5">
               <label class="form-label text-muted fw-semibold small text-uppercase">Password</label>
               <input type="password" class="form-control form-control-lg bg-light border-0 px-4" v-model="form.password" required style="border-radius: 8px;">
             </div>
             <button type="submit" class="btn btn-success btn-lg w-100 shadow-sm fw-bold" :disabled="loading" style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); border: none; border-radius: 8px;">
               {{ loading ? 'Registering...' : 'Register Company' }}
             </button>
             <p class="text-muted mt-4 text-center small text-uppercase fw-semibold">Note: Your account will require Admin approval before you can login.</p>
          </form>
          
          <div class="text-center mt-3">
            <p class="text-muted mb-0">Already have an account? <router-link to="/login" class="text-success fw-semibold text-decoration-none">Sign In</router-link></p>
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
  company_name: '', hr_contact: '', website: '', email: '', password: ''
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
    const res = await axios.post('/auth/register/company', form)
    successMsg.value = res.data.msg + ' Redirecting to login...'
    setTimeout(() => router.push('/login'), 3000)
  } catch (err) {
    errorMsg.value = err.response?.data?.msg || 'Registration failed'
  } finally {
    loading.value = false
  }
}
</script>
