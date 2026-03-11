import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../store/auth'

const routes = [
  { path: '/', component: () => import('../views/Home.vue') },
  { path: '/login', component: () => import('../views/Login.vue') },
  { path: '/register/student', component: () => import('../views/RegisterStudent.vue') },
  { path: '/register/company', component: () => import('../views/RegisterCompany.vue') },
  { 
    path: '/admin', 
    component: () => import('../views/admin/Dashboard.vue'),
    meta: { requiresAuth: true, role: 'admin' }
  },
  { 
    path: '/company', 
    component: () => import('../views/company/Dashboard.vue'),
    meta: { requiresAuth: true, role: 'company' }
  },
  { 
    path: '/student', 
    component: () => import('../views/student/Dashboard.vue'),
    meta: { requiresAuth: true, role: 'student' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  if (to.meta.requiresAuth && !authStore.token) {
    return next('/login')
  }
  if (to.meta.role && authStore.role !== to.meta.role) {
    return next('/')
  }
  next()
})

export default router
