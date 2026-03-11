<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary shadow-sm" style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%) !important;">
      <div class="container">
        <router-link class="navbar-brand fw-bold" to="/">Placement Portal</router-link>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarsExample">
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarsExample">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <template v-if="authStore.token">
              <li class="nav-item" v-if="authStore.role === 'admin'">
                <router-link class="nav-link" to="/admin">Admin Dashboard</router-link>
              </li>
              <li class="nav-item" v-if="authStore.role === 'company'">
                <router-link class="nav-link" to="/company">Company Dashboard</router-link>
              </li>
              <li class="nav-item" v-if="authStore.role === 'student'">
                <router-link class="nav-link" to="/student">Student Dashboard</router-link>
              </li>
            </template>
          </ul>
          <div class="d-flex">
            <template v-if="!authStore.token">
              <router-link class="btn btn-outline-light me-2" to="/login">Login</router-link>
              <div class="dropdown">
                 <button class="btn btn-warning dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                   Register
                 </button>
                 <ul class="dropdown-menu">
                   <li><router-link class="dropdown-item" to="/register/student">Student</router-link></li>
                   <li><router-link class="dropdown-item" to="/register/company">Company</router-link></li>
                 </ul>
              </div>
            </template>
            <template v-else>
              <button class="btn btn-danger" @click="logout">Logout</button>
            </template>
          </div>
        </div>
      </div>
    </nav>
    <div class="container mt-4">
      <router-view></router-view>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from './store/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const logout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
body {
  background-color: #f8f9fa;
  font-family: 'Inter', sans-serif;
}
.navbar {
  transition: all 0.3s ease;
}
</style>
