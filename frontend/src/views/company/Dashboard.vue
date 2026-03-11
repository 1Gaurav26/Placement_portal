<template>
  <div>
    <h2 class="mb-4">Company Dashboard <span v-if="stats.company_name" class="text-muted fw-light">| {{ stats.company_name }}</span></h2>
    
    <div v-if="errorMsg" class="alert alert-danger">{{ errorMsg }}</div>

    <div v-else>
      <div class="row mb-5 text-center">
        <div class="col-md-6 mb-3">
          <div class="card text-white bg-primary shadow-sm h-100" style="border-radius: 15px;">
            <div class="card-body py-4">
              <h5 class="card-title fw-semibold">Total Drives Hosted</h5>
              <h2 class="display-4 fw-bold">{{ stats.total_drives }}</h2>
            </div>
          </div>
        </div>
        <div class="col-md-6 mb-3">
          <div class="card text-white bg-info shadow-sm h-100" style="border-radius: 15px;">
            <div class="card-body py-4">
              <h5 class="card-title fw-semibold">Total Applications Received</h5>
              <h2 class="display-4 fw-bold">{{ stats.total_applications }}</h2>
            </div>
          </div>
        </div>
      </div>

      <!-- Upcoming Drives -->
      <div class="d-flex justify-content-between align-items-center mb-3">
        <h4>Upcoming Drives</h4>
        <button class="btn btn-success fw-bold px-4" data-bs-toggle="modal" data-bs-target="#createDriveModal">
          + Create New Drive
        </button>
      </div>

      <div class="table-responsive bg-white rounded shadow p-3 border-0 mb-5">
        <table class="table table-hover align-middle mb-0">
          <thead class="table-light text-muted">
            <tr>
              <th>SR NO</th>
              <th>JOB TITLE</th>
              <th>DEADLINE</th>
              <th>STATUS</th>
              <th>APPLICANTS</th>
              <th>ACTIONS</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(d, index) in upcomingDrives" :key="d.id">
              <td>{{ index + 1 }}</td>
              <td class="fw-semibold text-dark">{{ d.job_title }}</td>
              <td>{{ d.deadline }}</td>
              <td>
                 <span class="badge" :class="statusClass(d.status)">{{ d.status.toUpperCase() }}</span>
              </td>
              <td>{{ d.applications_count }}</td>
              <td>
                <button class="btn btn-sm btn-outline-primary me-1" @click="viewApplicants(d.id)" data-bs-toggle="modal" data-bs-target="#applicantsModal">View Details</button>
                <button v-if="d.status === 'approved'" class="btn btn-sm btn-outline-dark" @click="completeDrive(d.id)">Mark Complete</button>
              </td>
            </tr>
            <tr v-if="upcomingDrives.length === 0">
              <td colspan="6" class="text-center text-muted py-4">No upcoming drives.</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Closed Drives -->
      <h4 class="mb-3">Closed Drives</h4>
      <div class="table-responsive bg-white rounded shadow p-3 border-0 mb-5">
        <table class="table table-hover align-middle mb-0">
          <thead class="table-light text-muted">
            <tr>
              <th>SR NO</th>
              <th>JOB TITLE</th>
              <th>DEADLINE</th>
              <th>STATUS</th>
              <th>ACTIONS</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(d, index) in closedDrives" :key="d.id">
              <td>{{ index + 1 }}</td>
              <td class="fw-semibold text-dark">{{ d.job_title }}</td>
              <td>{{ d.deadline }}</td>
              <td><span class="badge bg-dark">CLOSED</span></td>
              <td>
                <button class="btn btn-sm btn-outline-warning" @click="unpublishDrive(d.id)">Unpublish</button>
              </td>
            </tr>
            <tr v-if="closedDrives.length === 0">
              <td colspan="5" class="text-center text-muted py-4">No closed drives.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Create Drive Modal -->
    <div class="modal fade" id="createDriveModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content border-0 shadow">
          <div class="modal-header bg-light">
            <h5 class="modal-title fw-bold">Create Placement Drive</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="createDrive">
               <div class="mb-3">
                 <label class="form-label text-muted fw-semibold">Job Title</label>
                 <input type="text" class="form-control" v-model="newDrive.job_title" required>
               </div>
               <div class="mb-3">
                 <label class="form-label text-muted fw-semibold">Description</label>
                 <textarea class="form-control" rows="3" v-model="newDrive.description" required></textarea>
               </div>
               <div class="row">
                 <div class="col-md-6 mb-3">
                   <label class="form-label text-muted fw-semibold">Min CGPA</label>
                   <input type="number" step="0.01" class="form-control" v-model="newDrive.min_cgpa" required>
                 </div>
                 <div class="col-md-6 mb-3">
                   <label class="form-label text-muted fw-semibold">Deadline (YYYY-MM-DD)</label>
                   <input type="date" class="form-control" v-model="newDrive.deadline" required>
                 </div>
               </div>
               <div class="mb-3">
                 <label class="form-label text-muted fw-semibold">Allowed Branches (comma separated, or 'ANY')</label>
                 <input type="text" class="form-control" v-model="newDrive.allowed_branches" required placeholder="CSE, ECE, IT">
               </div>
               <div class="row">
                 <div class="col-md-6 mb-3">
                   <label class="form-label text-muted fw-semibold">Salary</label>
                   <input type="text" class="form-control" v-model="newDrive.salary" placeholder="e.g. 600000">
                 </div>
                 <div class="col-md-6 mb-3">
                   <label class="form-label text-muted fw-semibold">Location</label>
                   <input type="text" class="form-control" v-model="newDrive.location" placeholder="e.g. Chennai">
                 </div>
               </div>
               <button type="submit" class="btn btn-success w-100 fw-bold py-2">Submit Drive for Approval</button>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Applicants Modal -->
    <div class="modal fade" id="applicantsModal" tabindex="-1">
      <div class="modal-dialog modal-xl">
        <div class="modal-content border-0 shadow">
          <div class="modal-header bg-light">
            <h5 class="modal-title fw-bold">Applicants List</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body bg-light">
            <div class="table-responsive bg-white rounded shadow-sm p-3 border-0">
              <table class="table table-hover align-middle mb-0">
                <thead class="table-light">
                  <tr>
                    <th>STUDENT NAME</th>
                    <th>BRANCH</th>
                    <th>CGPA</th>
                    <th>APPLIED DATE</th>
                    <th>STATUS</th>
                    <th>UPDATE STATUS</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="app in applicants" :key="app.id">
                    <td class="fw-semibold">{{ app.student_name }}
                      <br><a v-if="app.resume_url" :href="app.resume_url" target="_blank" class="small text-decoration-none">View Resume</a>
                    </td>
                    <td>{{ app.student_branch }}</td>
                    <td><span class="badge bg-secondary">{{ app.student_cgpa }}</span></td>
                    <td>{{ app.applied_at.split('T')[0] }}</td>
                    <td>
                      <span class="badge" :class="statusClass(app.status)">{{ app.status.toUpperCase() }}</span>
                    </td>
                    <td>
                      <select class="form-select form-select-sm d-inline-block w-auto shadow-sm" @change="updateStatus(app.id, $event.target.value)">
                        <option value="" selected disabled>Action</option>
                        <option value="shortlisted">Shortlist</option>
                        <option value="selected">Select</option>
                        <option value="rejected">Reject</option>
                      </select>
                    </td>
                  </tr>
                  <tr v-if="applicants.length === 0">
                     <td colspan="6" class="text-center text-muted py-4">No applicants yet.</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const stats = ref({ total_drives: 0, total_applications: 0, company_name: '' })
const drives = ref([])
const applicants = ref([])
const errorMsg = ref('')

const newDrive = ref({
  job_title: '', description: '', min_cgpa: 7.0, allowed_branches: 'ANY', deadline: '', salary: '', location: ''
})

const upcomingDrives = computed(() => drives.value.filter(d => d.status !== 'closed'))
const closedDrives = computed(() => drives.value.filter(d => d.status === 'closed'))

onMounted(() => {
  fetchDashboard()
  fetchDrives()
})

const statusClass = (status) => {
  if (status === 'approved' || status === 'selected') return 'bg-success'
  if (status === 'pending' || status === 'applied') return 'bg-warning text-dark'
  if (status === 'rejected') return 'bg-danger'
  if (status === 'shortlisted') return 'bg-info'
  if (status === 'closed') return 'bg-dark'
  return 'bg-secondary'
}

const fetchDashboard = async () => {
  try {
    const res = await axios.get('/company/dashboard')
    stats.value = res.data
  } catch (err) {
    if (err.response?.status === 403) {
      errorMsg.value = err.response.data.msg
    }
  }
}

const fetchDrives = async () => {
  try {
    const res = await axios.get('/company/drives')
    drives.value = res.data
  } catch (err) { }
}

const createDrive = async () => {
  try {
    await axios.post('/company/drives', newDrive.value)
    alert("Drive created and pending admin approval")
    newDrive.value = { job_title: '', description: '', min_cgpa: 7.0, allowed_branches: 'ANY', deadline: '', salary: '', location: '' }
    document.querySelector('#createDriveModal .btn-close').click()
    fetchDrives()
    fetchDashboard()
  } catch (err) { alert(err.response?.data?.msg || "Error creating drive") }
}

const viewApplicants = async (drive_id) => {
  applicants.value = []
  try {
    const res = await axios.get(`/company/drives/${drive_id}/applications`)
    applicants.value = res.data
  } catch (err) { }
}

const updateStatus = async (app_id, status) => {
  try {
    await axios.post(`/company/applications/${app_id}/status`, { status })
    const index = applicants.value.findIndex(a => a.id === app_id)
    if (index !== -1) {
      applicants.value[index].status = status
    }
    fetchDashboard()
  } catch (err) { alert("Error changing status") }
}

const completeDrive = async (drive_id) => {
  try {
    await axios.post(`/company/drives/${drive_id}/complete`)
    fetchDrives()
    fetchDashboard()
  } catch (err) { alert("Error completing drive") }
}

const unpublishDrive = async (drive_id) => {
  try {
    await axios.post(`/company/drives/${drive_id}/unpublish`)
    fetchDrives()
    fetchDashboard()
  } catch (err) { alert("Error unpublishing drive") }
}
</script>
