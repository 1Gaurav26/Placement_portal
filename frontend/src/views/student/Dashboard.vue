<template>
  <div>
    <h2 class="mb-4">Student Dashboard <span v-if="profile.first_name" class="text-muted fw-light">| Welcome, {{ profile.first_name }}</span></h2>
    
    <ul class="nav nav-pills mb-4 gap-2" id="studentTabs" role="tablist">
      <li class="nav-item" role="presentation">
        <button class="nav-link active fw-bold" data-bs-toggle="pill" data-bs-target="#available" type="button" role="tab" @click="fetchAvailableDrives">Available Drives</button>
      </li>
      <li class="nav-item" role="presentation">
        <button class="nav-link fw-bold" data-bs-toggle="pill" data-bs-target="#organizations" type="button" role="tab" @click="fetchCompanies">Organizations</button>
      </li>
      <li class="nav-item" role="presentation">
        <button class="nav-link fw-bold" data-bs-toggle="pill" data-bs-target="#applied" type="button" role="tab" @click="fetchApplications">My Applications</button>
      </li>
      <li class="nav-item" role="presentation">
        <button class="nav-link fw-bold" data-bs-toggle="pill" data-bs-target="#profile" type="button" role="tab" @click="fetchProfile">My Profile</button>
      </li>
    </ul>

    <div class="tab-content" id="studentTabsContent">
      
      <!-- Available Drives -->
      <div class="tab-pane fade show active" id="available" role="tabpanel">
        <div class="row">
          <div class="col-md-6 mb-4" v-for="d in availableDrives" :key="d.id">
            <div class="card shadow-sm h-100 border-0 hover-card" style="border-radius: 15px;">
              <div class="card-body p-4">
                <h5 class="card-title text-primary fw-bold mb-1">{{ d.job_title }}</h5>
                <h6 class="card-subtitle mb-3 text-muted">{{ d.company_name }}</h6>
                <p class="card-text text-secondary mb-4">{{ d.description.substring(0, 100) }}...</p>
                <div class="d-flex justify-content-between align-items-center">
                  <span class="small text-danger fw-semibold">Deadline: {{ d.deadline }}</span>
                  <div>
                    <button class="btn btn-outline-info btn-sm me-1" @click="viewDriveDetail(d.id)">View Details</button>
                    <button v-if="d.has_applied" class="btn btn-secondary btn-sm" disabled>Applied</button>
                    <button v-else-if="!d.is_eligible" class="btn btn-outline-danger btn-sm" disabled>Not Eligible ({{ d.ineligibility_reason }})</button>
                    <button v-else class="btn btn-primary btn-sm fw-bold px-4" @click="applyForDrive(d.id)">Apply Now</button>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div v-if="availableDrives.length === 0" class="col-12 text-center py-5">
            <h5 class="text-muted">No placement drives available right now.</h5>
          </div>
        </div>
      </div>

      <!-- Organizations -->
      <div class="tab-pane fade" id="organizations" role="tabpanel">
        <div class="table-responsive bg-white rounded shadow p-3 border-0">
          <table class="table table-hover align-middle mb-0">
            <thead class="table-light text-muted">
              <tr>
                <th>COMPANY NAME</th>
                <th>HR CONTACT</th>
                <th>WEBSITE</th>
                <th>ACTIONS</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="c in companies" :key="c.id">
                <td class="fw-semibold text-dark">{{ c.name }}</td>
                <td>{{ c.hr_contact }}</td>
                <td><a v-if="c.website" :href="c.website" target="_blank" class="text-decoration-none">{{ c.website }}</a></td>
                <td>
                  <button class="btn btn-sm btn-outline-primary" @click="viewCompanyDetail(c.id)" data-bs-toggle="modal" data-bs-target="#companyDetailModal">View Details</button>
                </td>
              </tr>
              <tr v-if="companies.length === 0">
                <td colspan="4" class="text-center text-muted py-4">No organizations found.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- My Applications -->
      <div class="tab-pane fade" id="applied" role="tabpanel">
        <!-- Trigger Export Job -->
        <div class="d-flex justify-content-end mb-3">
          <button class="btn btn-outline-primary fw-bold" @click="exportApplications" :disabled="exporting">
            {{ exporting ? 'Exporting...' : 'Export as CSV (Email Trigger)' }}
          </button>
        </div>
        <div class="table-responsive bg-white rounded shadow p-3 border-0">
          <table class="table table-hover align-middle mb-0">
            <thead class="table-light text-muted">
              <tr>
                <th>SR NO</th>
                <th>COMPANY</th>
                <th>JOB TITLE</th>
                <th>APPLIED DATE</th>
                <th>INTERVIEW</th>
                <th>STATUS</th>
                <th>REMARK</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(app, index) in applications" :key="app.id">
                <td>{{ index + 1 }}</td>
                <td class="fw-semibold text-dark">{{ app.company_name }}</td>
                <td class="fw-semibold">{{ app.job_title }}</td>
                <td>{{ app.applied_at.split('T')[0] }}</td>
                <td>{{ app.interview_type }}</td>
                <td>
                  <span class="badge" :class="statusClass(app.status)">{{ app.status.toUpperCase() }}</span>
                </td>
                <td>{{ app.remark || '-' }}</td>
              </tr>
              <tr v-if="applications.length === 0">
                <td colspan="7" class="text-center text-muted py-4">You have not applied to any drives yet.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Profile Tab -->
      <div class="tab-pane fade" id="profile" role="tabpanel">
        <div class="card shadow-sm border-0" style="border-radius: 15px;">
          <div class="card-body p-5">
            <h4 class="mb-4 text-primary fw-bold">Edit Profile</h4>
            <div v-if="profileMsg" class="alert alert-success">{{ profileMsg }}</div>
            <form @submit.prevent="updateProfile">
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label text-muted fw-semibold">First Name</label>
                  <input type="text" class="form-control" v-model="profile.first_name" required>
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label text-muted fw-semibold">Last Name</label>
                  <input type="text" class="form-control" v-model="profile.last_name" required>
                </div>
              </div>
              <div class="row">
                <div class="col-md-4 mb-3">
                  <label class="form-label text-muted fw-semibold">Branch</label>
                  <input type="text" class="form-control" v-model="profile.branch" required>
                </div>
                <div class="col-md-4 mb-3">
                  <label class="form-label text-muted fw-semibold">CGPA</label>
                  <input type="number" step="0.01" class="form-control" v-model="profile.cgpa" required>
                </div>
                <div class="col-md-4 mb-3">
                  <label class="form-label text-muted fw-semibold">Graduation Year</label>
                  <input type="number" class="form-control" v-model="profile.graduation_year" disabled>
                </div>
              </div>
              <div class="mb-4">
                <label class="form-label text-muted fw-semibold">Resume URL</label>
                <input type="url" class="form-control" v-model="profile.resume_url" placeholder="Link to your Google Drive or Github resume">
              </div>
              <button type="submit" class="btn btn-primary px-5 fw-bold">Save Changes</button>
            </form>
          </div>
        </div>
      </div>

    </div>

    <!-- Company Detail Modal -->
    <div class="modal fade" id="companyDetailModal" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content border-0 shadow">
          <div class="modal-header bg-light">
            <h5 class="modal-title fw-bold">{{ companyDetail.name }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <p><strong>HR Contact:</strong> {{ companyDetail.hr_contact }}</p>
            <p><strong>Website:</strong> <a :href="companyDetail.website" target="_blank">{{ companyDetail.website }}</a></p>
            
            <h5 class="mt-4 mb-3 fw-bold">Current Drives</h5>
            <div class="table-responsive">
              <table class="table table-hover align-middle mb-0">
                <thead class="table-light text-muted">
                  <tr>
                    <th>DRIVE</th>
                    <th>DEADLINE</th>
                    <th>ACTIONS</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="d in companyDetail.drives" :key="d.id">
                    <td class="fw-semibold text-dark">{{ d.job_title }}</td>
                    <td>{{ d.deadline }}</td>
                    <td>
                      <button class="btn btn-sm btn-outline-primary" @click="viewDriveDetail(d.id)" data-bs-dismiss="modal">View Details</button>
                    </td>
                  </tr>
                  <tr v-if="!companyDetail.drives || companyDetail.drives.length === 0">
                    <td colspan="3" class="text-center text-muted py-3">No active drives.</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Drive Detail Modal -->
    <div class="modal fade" id="driveDetailModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content border-0 shadow">
          <div class="modal-header bg-light">
            <h5 class="modal-title fw-bold">Drive Details</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body" v-if="driveDetail">
            <h4 class="text-primary fw-bold mb-1">{{ driveDetail.job_title }}</h4>
            <h6 class="text-muted mb-3">{{ driveDetail.company_name }}</h6>
            
            <p class="text-secondary">{{ driveDetail.description }}</p>
            
            <div class="row mt-3">
              <div class="col-6 mb-2"><strong>Min CGPA:</strong> {{ driveDetail.min_cgpa }}</div>
              <div class="col-6 mb-2"><strong>Branches:</strong> {{ driveDetail.allowed_branches }}</div>
              <div class="col-6 mb-2"><strong>Salary:</strong> {{ driveDetail.salary || 'Not specified' }}</div>
              <div class="col-6 mb-2"><strong>Location:</strong> {{ driveDetail.location || 'Not specified' }}</div>
              <div class="col-12 mb-2"><strong>Deadline:</strong> <span class="text-danger">{{ driveDetail.deadline }}</span></div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Go Back</button>
            <button v-if="driveDetail && !driveDetail.has_applied" class="btn btn-primary fw-bold px-4" @click="applyFromDetail(driveDetail.id)">Apply</button>
            <button v-else class="btn btn-secondary" disabled>Already Applied</button>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { Modal } from 'bootstrap'

const availableDrives = ref([])
const applications = ref([])
const companies = ref([])
const companyDetail = ref({ name: '', hr_contact: '', website: '', drives: [] })
const driveDetail = ref(null)
const profile = ref({
  first_name: '', last_name: '', branch: '', cgpa: 0, graduation_year: 2024, resume_url: ''
})
const profileMsg = ref('')
const exporting = ref(false)

onMounted(() => {
  fetchProfile()
  fetchAvailableDrives()
  fetchApplications()
})

const statusClass = (status) => {
  if (status === 'approved' || status === 'selected') return 'bg-success'
  if (status === 'pending' || status === 'applied') return 'bg-warning text-dark'
  if (status === 'rejected') return 'bg-danger'
  if (status === 'shortlisted') return 'bg-info'
  return 'bg-secondary'
}

const fetchAvailableDrives = async () => {
  try {
    const res = await axios.get('/student/dashboard')
    availableDrives.value = res.data
  } catch (err) { }
}

const applyForDrive = async (id) => {
  if (!confirm("Are you sure you want to apply?")) return
  try {
    await axios.post(`/student/drives/${id}/apply`)
    alert("Application successful!")
    fetchAvailableDrives()
    fetchApplications()
  } catch (err) { alert(err.response?.data?.msg || "Error applying") }
}

const fetchApplications = async () => {
  try {
    const res = await axios.get('/student/applications')
    applications.value = res.data
  } catch (err) { }
}

const fetchProfile = async () => {
  try {
    const res = await axios.get('/student/profile')
    profile.value = res.data
  } catch (err) { }
}

const updateProfile = async () => {
  profileMsg.value = ''
  try {
    const res = await axios.put('/student/profile', profile.value)
    profileMsg.value = "Profile updated successfully!"
  } catch (err) { alert("Error updating profile") }
}

const exportApplications = async () => {
  exporting.value = true
  try {
    const res = await axios.post('/student/tasks/export-csv')
    alert(res.data.msg)
  } catch(err) {
    alert("Export triggered")
  } finally {
    exporting.value = false
  }
}

const fetchCompanies = async () => {
  try {
    const res = await axios.get('/student/companies')
    companies.value = res.data
  } catch (err) { }
}

const viewCompanyDetail = async (companyId) => {
  try {
    const res = await axios.get(`/student/companies/${companyId}`)
    companyDetail.value = res.data
  } catch (err) { }
}

const viewDriveDetail = async (driveId) => {
  try {
    const res = await axios.get(`/student/drives/${driveId}`)
    driveDetail.value = res.data
    const modalEl = document.getElementById('driveDetailModal')
    const modal = new Modal(modalEl)
    modal.show()
  } catch (err) { alert("Error loading drive details") }
}

const applyFromDetail = async (driveId) => {
  if (!confirm("Are you sure you want to apply?")) return
  try {
    await axios.post(`/student/drives/${driveId}/apply`)
    alert("Application successful!")
    document.querySelector('#driveDetailModal .btn-close').click()
    fetchAvailableDrives()
    fetchApplications()
  } catch (err) { alert(err.response?.data?.msg || "Error applying") }
}
</script>

<style scoped>
.hover-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.hover-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 .5rem 1rem rgba(0,0,0,.15)!important;
}
</style>
