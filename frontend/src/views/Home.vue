<template>
  <div class="row text-center mt-5">
    <div class="col-md-12">
      <h1 class="display-4 fw-bold mb-4" style="color: #2a5298;">Welcome to Campus Placement Portal</h1>
      <p class="lead mb-5 text-muted">A unified platform for Institutes, Companies, and Students to streamline recruitment and foster careers.</p>
    </div>

    <div class="col-md-4">
      <div class="card shadow-sm border-0 h-100 hover-card">
        <div class="card-body py-5">
          <h3 class="card-title text-primary">For Institutes</h3>
          <p class="card-text text-muted">Manage companies, track placement drives, view statistics and reports effortlessly.</p>
        </div>
      </div>
    </div>
    <div class="col-md-4">
      <div class="card shadow-sm border-0 h-100 hover-card">
        <div class="card-body py-5">
          <h3 class="card-title text-success">For Companies</h3>
          <p class="card-text text-muted">Host recruitment drives, shortlist candidates and schedule interviews seamlessly.</p>
        </div>
      </div>
    </div>
    <div class="col-md-4">
      <div class="card shadow-sm border-0 h-100 hover-card">
        <div class="card-body py-5">
          <h3 class="card-title text-warning">For Students</h3>
          <p class="card-text text-muted">Apply for top placement drives, view application statuses, and track your jobs.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.hover-card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border-radius: 15px;
}
.hover-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 1rem 3rem rgba(0,0,0,.175)!important;
}
</style>
