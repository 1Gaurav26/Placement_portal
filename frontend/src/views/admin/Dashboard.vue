<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>Admin Dashboard</h2>
      <div class="d-flex gap-2">
        <input type="text" class="form-control" placeholder="Search students & companies..." v-model="searchQuery" @keyup.enter="performSearch" style="width: 280px;">
        <button class="btn btn-primary fw-bold px-4" @click="performSearch">Search</button>
      </div>
    </div>

    <!-- Search Results -->
    <div v-if="searchResults" class="mb-4">
      <div class="card border-0 shadow-sm" style="border-radius: 15px;">
        <div class="card-body">
          <div class="d-flex justify-content-between align-items-center mb-3">
            <h5 class="fw-bold mb-0">Search Results for "{{ searchQuery }}"</h5>
            <button class="btn btn-sm btn-outline-secondary" @click="searchResults = null; searchQuery = ''">Clear</button>
          </div>
          <div class="row">
            <div class="col-md-6">
              <h6 class="text-muted fw-semibold">Students</h6>
              <ul class="list-group list-group-flush" v-if="searchResults.students.length">
                <li v-for="s in searchResults.students" :key="s.id" class="list-group-item d-flex justify-content-between">
                  <span>{{ s.name }}</span>
                  <span class="badge bg-secondary">{{ s.branch }} | {{ s.cgpa }}</span>
                </li>
              </ul>
              <p v-else class="text-muted small">No students found.</p>
            </div>
            <div class="col-md-6">
              <h6 class="text-muted fw-semibold">Companies</h6>
              <ul class="list-group list-group-flush" v-if="searchResults.companies.length">
                <li v-for="c in searchResults.companies" :key="c.id" class="list-group-item d-flex justify-content-between">
                  <span>{{ c.name }}</span>
                  <span class="badge" :class="statusClass(c.approval_status)">{{ c.approval_status.toUpperCase() }}</span>
                </li>
              </ul>
              <p v-else class="text-muted small">No companies found.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div class="row mb-5 text-center">
      <div class="col-md-4 mb-3">
        <div class="card text-white bg-primary shadow-sm h-100" style="border-radius: 15px;">
          <div class="card-body py-4">
            <h5 class="card-title fw-semibold">Total Students</h5>
            <h2 class="display-4 fw-bold">{{ stats.total_students }}</h2>
          </div>
        </div>
      </div>
      <div class="col-md-4 mb-3">
        <div class="card text-white bg-success shadow-sm h-100" style="border-radius: 15px;">
          <div class="card-body py-4">
            <h5 class="card-title fw-semibold">Total Companies</h5>
            <h2 class="display-4 fw-bold">{{ stats.total_companies }}</h2>
          </div>
        </div>
      </div>
      <div class="col-md-4 mb-3">
        <div class="card text-white bg-info shadow-sm h-100" style="border-radius: 15px;">
          <div class="card-body py-4">
            <h5 class="card-title fw-semibold">Total Drives</h5>
            <h2 class="display-4 fw-bold">{{ stats.total_drives }}</h2>
          </div>
        </div>
      </div>
    </div>

    <ul class="nav nav-pills mb-4 gap-2" id="adminTabs" role="tablist">
      <li class="nav-item" role="presentation">
        <button class="nav-link active fw-bold" data-bs-toggle="pill" data-bs-target="#companies" type="button" role="tab" @click="fetchCompanies">Manage Companies</button>
      </li>
      <li class="nav-item" role="presentation">
        <button class="nav-link fw-bold" data-bs-toggle="pill" data-bs-target="#drives" type="button" role="tab" @click="fetchDrives">Manage Drives</button>
      </li>
      <li class="nav-item" role="presentation">
        <button class="nav-link fw-bold" data-bs-toggle="pill" data-bs-target="#students" type="button" role="tab" @click="fetchStudents">Registered Students</button>
      </li>
      <li class="nav-item" role="presentation">
        <button class="nav-link fw-bold" data-bs-toggle="pill" data-bs-target="#applications" type="button" role="tab" @click="fetchApplications">Student Applications</button>
      </li>
    </ul>

    <div class="tab-content" id="adminTabsContent">
      <!-- Companies Tab -->
      <div class="tab-pane fade show active" id="companies" role="tabpanel">
        <div class="table-responsive bg-white rounded shadow p-3 border-0">
          <table class="table table-hover align-middle mb-0">
            <thead class="table-light text-muted">
              <tr>
                <th>COMPANY NAME</th>
                <th>HR CONTACT</th>
                <th>WEBSITE</th>
                <th>STATUS</th>
                <th>ACCOUNT</th>
                <th>ACTIONS</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="c in companies" :key="c.id">
                <td class="fw-semibold text-dark">{{ c.name }}</td>
                <td>{{ c.hr_contact }}</td>
                <td><a :href="c.website" target="_blank" class="text-decoration-none">{{ c.website }}</a></td>
                <td>
                  <span class="badge" :class="statusClass(c.approval_status)">{{ c.approval_status.toUpperCase() }}</span>
                </td>
                <td>
                  <span v-if="c.active" class="badge bg-success">Active</span>
                  <span v-else class="badge bg-danger">Blacklisted</span>
                </td>
                <td>
                  <button v-if="c.approval_status === 'pending'" @click="approveCompany(c.id)" class="btn btn-sm btn-outline-success me-2 w-100 mb-1">Approve</button>
                  <button v-if="c.approval_status === 'pending'" @click="rejectCompany(c.id)" class="btn btn-sm btn-outline-danger me-2 w-100 mb-1">Reject</button>
                  <button @click="toggleUser(c.user_id)" class="btn btn-sm w-100" :class="c.active ? 'btn-outline-dark' : 'btn-dark'">
                    {{ c.active ? 'Blacklist' : 'Activate' }}
                  </button>
                </td>
              </tr>
              <tr v-if="companies.length === 0">
                <td colspan="6" class="text-center text-muted py-4">No companies found.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Drives Tab -->
      <div class="tab-pane fade" id="drives" role="tabpanel">
        <div class="table-responsive bg-white rounded shadow p-3 border-0">
          <table class="table table-hover align-middle mb-0">
            <thead class="table-light text-muted">
              <tr>
                <th>COMPANY</th>
                <th>JOB TITLE</th>
                <th>DEADLINE</th>
                <th>STATUS</th>
                <th>ACTIONS</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="d in drives" :key="d.id">
                <td class="fw-semibold text-dark">{{ d.company_name }}</td>
                <td class="fw-semibold">{{ d.job_title }}</td>
                <td>{{ d.deadline.split('T')[0] }}</td>
                <td>
                  <span class="badge" :class="statusClass(d.status)">{{ d.status.toUpperCase() }}</span>
                </td>
                <td>
                  <button v-if="d.status === 'pending'" @click="approveDrive(d.id)" class="btn btn-sm btn-outline-success me-1">Approve</button>
                  <button v-if="d.status === 'pending'" @click="rejectDrive(d.id)" class="btn btn-sm btn-outline-danger me-1">Reject</button>
                  <button v-if="d.status === 'approved'" @click="completeDrive(d.id)" class="btn btn-sm btn-outline-dark">Mark Complete</button>
                </td>
              </tr>
              <tr v-if="drives.length === 0">
                <td colspan="5" class="text-center text-muted py-4">No drives found.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Students Tab -->
      <div class="tab-pane fade" id="students" role="tabpanel">
        <div class="table-responsive bg-white rounded shadow p-3 border-0">
          <table class="table table-hover align-middle mb-0">
            <thead class="table-light text-muted">
              <tr>
                <th>NAME</th>
                <th>EMAIL</th>
                <th>BRANCH</th>
                <th>CGPA</th>
                <th>GRAD YEAR</th>
                <th>ACCOUNT</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="s in students" :key="s.id">
                <td class="fw-semibold text-dark">{{ s.first_name }} {{ s.last_name }}</td>
                <td>{{ s.email }}</td>
                <td><span class="badge bg-info text-dark">{{ s.branch }}</span></td>
                <td><span class="badge bg-secondary">{{ s.cgpa }}</span></td>
                <td>{{ s.graduation_year }}</td>
                <td>
                  <span v-if="s.active" class="badge bg-success">Active</span>
                  <span v-else class="badge bg-danger">Deactivated</span>
                </td>
              </tr>
              <tr v-if="students.length === 0">
                <td colspan="6" class="text-center text-muted py-4">No students found.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Applications Tab -->
      <div class="tab-pane fade" id="applications" role="tabpanel">
        <div class="table-responsive bg-white rounded shadow p-3 border-0">
          <table class="table table-hover align-middle mb-0">
            <thead class="table-light text-muted">
              <tr>
                <th>SR NO</th>
                <th>STUDENT NAME</th>
                <th>DRIVE</th>
                <th>COMPANY</th>
                <th>DATE</th>
                <th>STATUS</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(app, index) in allApplications" :key="app.id">
                <td>{{ index + 1 }}</td>
                <td class="fw-semibold text-dark">{{ app.student_name }}</td>
                <td>{{ app.job_title }}</td>
                <td>{{ app.company_name }}</td>
                <td>{{ app.applied_at.split('T')[0] }}</td>
                <td>
                  <span class="badge" :class="statusClass(app.status)">{{ app.status.toUpperCase() }}</span>
                </td>
              </tr>
              <tr v-if="allApplications.length === 0">
                <td colspan="6" class="text-center text-muted py-4">No applications found.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const stats = ref({ total_students: 0, total_companies: 0, total_drives: 0 })
const companies = ref([])
const drives = ref([])
const students = ref([])
const allApplications = ref([])
const searchQuery = ref('')
const searchResults = ref(null)

onMounted(() => {
  fetchStats()
  fetchCompanies()
})

const statusClass = (status) => {
  if (status === 'approved' || status === 'selected') return 'bg-success'
  if (status === 'pending' || status === 'applied') return 'bg-warning text-dark'
  if (status === 'rejected') return 'bg-danger'
  if (status === 'closed') return 'bg-dark'
  if (status === 'shortlisted') return 'bg-info'
  return 'bg-secondary'
}

const fetchStats = async () => {
  try {
    const res = await axios.get('/admin/dashboard')
    stats.value = res.data
  } catch (err) { console.error(err) }
}

const fetchCompanies = async () => {
  try {
    const res = await axios.get('/admin/companies')
    companies.value = res.data
  } catch (err) { console.error(err) }
}

const fetchDrives = async () => {
  try {
    const res = await axios.get('/admin/drives')
    drives.value = res.data
  } catch (err) { console.error(err) }
}

const fetchStudents = async () => {
  try {
    const res = await axios.get('/admin/students')
    students.value = res.data
  } catch (err) { console.error(err) }
}

const fetchApplications = async () => {
  try {
    const res = await axios.get('/admin/applications')
    allApplications.value = res.data
  } catch (err) { console.error(err) }
}

const approveCompany = async (id) => {
  await axios.post(`/admin/companies/${id}/approve`)
  fetchCompanies()
  fetchStats()
}

const rejectCompany = async (id) => {
  await axios.post(`/admin/companies/${id}/reject`)
  fetchCompanies()
}

const toggleUser = async (user_id) => {
  await axios.post(`/admin/users/${user_id}/toggle_status`)
  fetchCompanies()
}

const approveDrive = async (id) => {
  await axios.post(`/admin/drives/${id}/approve`)
  fetchDrives()
  fetchStats()
}

const rejectDrive = async (id) => {
  await axios.post(`/admin/drives/${id}/reject`)
  fetchDrives()
}

const completeDrive = async (id) => {
  await axios.post(`/admin/drives/${id}/complete`)
  fetchDrives()
  fetchStats()
}

const performSearch = async () => {
  if (!searchQuery.value.trim()) return
  try {
    const res = await axios.get(`/admin/search?q=${encodeURIComponent(searchQuery.value)}`)
    searchResults.value = res.data
  } catch (err) { console.error(err) }
}
</script>
