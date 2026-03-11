# Placement Portal Application — Project Report

---

## Author

| Field | Details |
|-------|---------|
| **Full Name** | `<< Your Full Name >>` |
| **Roll Number** | `<< Your Roll Number >>` |
| **Email** | `<< your_email@institute.edu >>` |
| **About** | `<< Add a couple of lines about yourself, e.g. "I am a 3rd year B.Tech Computer Science student with a keen interest in full-stack web development and backend systems." >>` |

---

## AI/LLM Usage

| Aspect | Details |
|--------|---------|
| **AI/LLM Used** | Google Gemini (via Antigravity AI coding assistant) |
| **Extent of Use** | AI was used to assist with scaffolding the project structure, generating boilerplate code for Flask routes and Vue components, debugging issues, and refining UI aesthetics. All final code was reviewed and adapted manually. |
| **Estimated AI Usage** | ~60–70% of the initial code generation was AI-assisted; the remaining 30–40% involved manual design decisions, integration, testing, and iterative refinement. |

---

## Description

The Placement Portal is a full-stack web application that streamlines campus placement activities for an institute. It enables **Administrators** to manage and approve companies and placement drives, **Companies** to register, create placement drives, and manage applicants, and **Students** to browse eligible drives, apply, and track their application status — all through role-based authenticated dashboards.

AI/LLM was used approximately 60–70% for code generation and scaffolding. The remaining effort involved manual architecture design, business logic validation, UI/UX polishing, and integration testing.

---

## Technologies Used

### Backend

| Technology | Purpose |
|------------|---------|
| **Python 3** | Core backend programming language |
| **Flask** | Lightweight web framework for building REST APIs |
| **Flask-SQLAlchemy** | ORM for database modelling and query abstraction |
| **Flask-JWT-Extended** | JWT-based authentication and role-based authorization |
| **Flask-CORS** | Handling Cross-Origin Resource Sharing for frontend-backend communication |
| **Flask-Caching** | Server-side response caching with Redis backend (e.g., student dashboard) |
| **Celery** | Distributed task queue for async/scheduled background jobs |
| **Redis** | Message broker for Celery and cache store for Flask-Caching |
| **Werkzeug** | Password hashing (`generate_password_hash` / `check_password_hash`) |
| **SQLite** | Lightweight relational database (development) |

### Frontend

| Technology | Purpose |
|------------|---------|
| **Vue.js 3** | Reactive SPA framework for building the UI |
| **Vite 7** | Next-generation frontend build tool and dev server |
| **Vue Router 5** | Client-side routing with route guards for auth/role checks |
| **Pinia 3** | State management (auth store for token/role persistence) |
| **Bootstrap 5** | CSS framework for responsive layout and UI components |
| **Axios** | HTTP client for API communication with the Flask backend |

---

## DB Schema Design

The application uses **5 tables** in an SQLite database. Below is the detailed schema:

### 1. `users`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | Integer | PRIMARY KEY, Auto-increment | Unique user identifier |
| `email` | String(120) | UNIQUE, NOT NULL | Login email address |
| `password_hash` | String(255) | NOT NULL | Werkzeug-hashed password |
| `role` | String(20) | NOT NULL | Role: `admin`, `company`, or `student` |
| `active` | Boolean | DEFAULT `True` | Account activation status (admin can toggle) |
| `created_at` | DateTime | DEFAULT `utcnow` | Account creation timestamp |

**Relationships:** One-to-one with `company_profiles` or `student_profiles` (cascading delete).

---

### 2. `company_profiles`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | Integer | PRIMARY KEY | Unique company profile ID |
| `user_id` | Integer | FK → `users.id`, NOT NULL | Link to the parent user account |
| `name` | String(150) | NOT NULL | Company name |
| `hr_contact` | String(100) | NOT NULL | HR contact person name |
| `website` | String(255) | NULLABLE | Company website URL |
| `approval_status` | String(20) | DEFAULT `pending` | Admin approval: `pending`, `approved`, `rejected` |

**Relationships:** One-to-many with `placement_drives` (cascading delete).

---

### 3. `student_profiles`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | Integer | PRIMARY KEY | Unique student profile ID |
| `user_id` | Integer | FK → `users.id`, NOT NULL | Link to the parent user account |
| `first_name` | String(100) | NOT NULL | Student's first name |
| `last_name` | String(100) | NOT NULL | Student's last name |
| `branch` | String(50) | NOT NULL | Academic branch (e.g., CSE, ECE) |
| `cgpa` | Float | NOT NULL | Cumulative GPA |
| `graduation_year` | Integer | NOT NULL | Expected graduation year |
| `resume_url` | String(255) | NULLABLE | Link to uploaded resume |

**Relationships:** One-to-many with `applications` (cascading delete).

---

### 4. `placement_drives`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | Integer | PRIMARY KEY | Unique drive ID |
| `company_id` | Integer | FK → `company_profiles.id`, NOT NULL | Hosting company |
| `job_title` | String(150) | NOT NULL | Position title |
| `description` | Text | NOT NULL | Job description |
| `min_cgpa` | Float | NOT NULL | Minimum CGPA eligibility |
| `allowed_branches` | String(255) | NOT NULL | Comma-separated allowed branches (e.g., `CSE,ECE,IT`) |
| `deadline` | DateTime | NOT NULL | Application deadline |
| `salary` | String(100) | NULLABLE | CTC / salary package |
| `location` | String(150) | NULLABLE | Job location |
| `status` | String(20) | DEFAULT `pending` | Drive status: `pending`, `approved`, `closed` |
| `created_at` | DateTime | DEFAULT `utcnow` | Drive creation timestamp |

**Relationships:** One-to-many with `applications` (cascading delete).

---

### 5. `applications`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | Integer | PRIMARY KEY | Unique application ID |
| `student_id` | Integer | FK → `student_profiles.id`, NOT NULL | Applying student |
| `drive_id` | Integer | FK → `placement_drives.id`, NOT NULL | Target placement drive |
| `status` | String(20) | DEFAULT `applied` | Status: `applied`, `shortlisted`, `selected`, `rejected` |
| `interview_type` | String(50) | DEFAULT `N/A` | Interview mode (In-person / Online) |
| `remark` | String(255) | DEFAULT `''` | Additional notes |
| `applied_at` | DateTime | DEFAULT `utcnow` | Application timestamp |

### Design Rationale

- **Normalized structure:** Users are separated from profiles to allow a single `User` model for authentication while profiles carry role-specific data.
- **Cascading deletes:** Ensures referential integrity — deleting a user automatically removes their profile, drives, and applications.
- **Approval workflows:** Both `company_profiles.approval_status` and `placement_drives.status` require admin approval before entities become visible, enforcing a gatekeeper pattern.
- **Flexible eligibility:** `allowed_branches` stored as a comma-separated string allows easy filtering without a many-to-many join table, keeping the schema simple for the project scope.

---

## API Design

The backend exposes a RESTful API organized into **4 blueprints**, each with its own URL prefix:

### Authentication (`/api/auth`)
- `POST /login` — Authenticate user, returns JWT + role
- `POST /register/student` — Register a new student account
- `POST /register/company` — Register a new company (pending admin approval)

### Admin (`/api/admin`)
- `GET /dashboard` — Aggregate stats (total students, companies, drives)
- `GET /companies` — List all companies with approval status
- `POST /companies/:id/approve` — Approve a company registration
- `POST /companies/:id/reject` — Reject a company registration
- `GET /drives` — List all placement drives
- `POST /drives/:id/approve` — Approve a placement drive
- `POST /drives/:id/reject` — Reject a placement drive
- `POST /drives/:id/complete` — Mark a drive as closed
- `GET /students` — List all registered students
- `GET /applications` — View all applications across all drives
- `POST /users/:id/toggle_status` — Activate/deactivate a user account
- `GET /search?q=` — Search students and companies by name

### Company (`/api/company`)
- `GET /dashboard` — Company-specific stats (drives count, application count)
- `GET /drives` — List own placement drives
- `POST /drives` — Create a new placement drive (pending approval)
- `GET /drives/:id/applications` — View applications for a specific drive
- `POST /applications/:id/status` — Update application status (shortlist/select/reject)
- `POST /drives/:id/complete` — Close a drive
- `POST /drives/:id/unpublish` — Revert a drive to pending

### Student (`/api/student`)
- `GET /dashboard` — List all approved drives with eligibility check (cached 60s)
- `POST /drives/:id/apply` — Apply to a drive
- `GET /applications` — View own applications and their statuses
- `GET|PUT /profile` — View/update student profile
- `GET /companies` — List all approved companies
- `GET /companies/:id` — View company detail with its active drives
- `GET /drives/:id` — View drive detail
- `POST /tasks/export-csv` — Trigger async CSV export of applications (Celery)

> **Note:** The full OpenAPI/YAML spec should be submitted separately.

---

## Architecture and Features

### Project Organization

The project follows a **decoupled SPA architecture** with a clear separation between the Flask backend and the Vue.js frontend:

```
placement/
├── backend/
│   ├── app.py              # Flask app factory, extension init, catch-all route
│   ├── config.py           # Configuration (DB URI, JWT, Redis, Celery)
│   ├── models.py           # SQLAlchemy ORM models (5 tables)
│   ├── celery_worker.py    # Celery app factory with Flask context
│   ├── tasks.py            # Async & scheduled tasks (CSV export, reminders, reports)
│   └── routes/
│       ├── auth.py         # Authentication blueprint (login, register)
│       ├── admin.py        # Admin-only endpoints (CRUD, approvals, search)
│       ├── company.py      # Company endpoints (drives, applications)
│       └── student.py      # Student endpoints (dashboard, apply, profile)
├── frontend/
│   ├── index.html          # Vite entry point
│   ├── vite.config.js      # Vite build configuration
│   └── src/
│       ├── main.js         # Vue app bootstrap (Pinia, Router, Bootstrap)
│       ├── App.vue         # Root component with navbar
│       ├── router/index.js # Route definitions with auth guards
│       ├── store/auth.js   # Pinia store for JWT token and role
│       └── views/
│           ├── Home.vue            # Landing page
│           ├── Login.vue           # Sign-in form
│           ├── RegisterStudent.vue # Student registration form
│           ├── RegisterCompany.vue # Company registration form
│           ├── admin/Dashboard.vue # Admin dashboard (companies, drives, students, apps)
│           ├── company/Dashboard.vue # Company dashboard (drives, applicants)
│           └── student/Dashboard.vue # Student dashboard (drives, applications, profile)
```

Controllers (route handlers) are organized into **Flask Blueprints** inside the `backend/routes/` directory. Each blueprint has a custom decorator (`admin_required`, `company_required`, `student_required`) that enforces role-based access. The frontend views are organized by role inside `frontend/src/views/`, and the Vue Router uses `meta.requiresAuth` and `meta.role` for client-side route guarding.

### Features Implemented

**Default / Core Features:**
- **Role-based Authentication & Authorization:** Three roles (Admin, Company, Student) with JWT-secured endpoints and per-role route guards on both backend and frontend.
- **Company Registration & Approval Workflow:** Companies register and wait for admin approval before they can post drives.
- **Placement Drive Management:** Companies create drives (with eligibility criteria like min CGPA and allowed branches), admins approve/reject/close them.
- **Student Application Flow:** Students view eligible drives, apply with one click, and track application status (applied → shortlisted → selected/rejected).
- **Admin Dashboard:** Centralized view with stats, manage companies, drives, students, applications, and a search feature.
- **Profile Management:** Students can view and update their profile and resume URL.

**Additional / Advanced Features:**
- **Async CSV Export (Celery):** Students can trigger a background job to export their application history to CSV. The task runs asynchronously via Celery with Redis as the message broker.
- **Scheduled Jobs (Celery Beat):** Daily deadline reminders for drives expiring within 24 hours, and monthly activity reports summarizing placements — both run automatically.
- **API Caching (Flask-Caching + Redis):** The student dashboard response is cached for 60 seconds to reduce database load on repeated requests.
- **User Account Management:** Admins can activate/deactivate any user account (except other admins).
- **Eligibility Engine:** Automatic eligibility checks against CGPA, branch, and deadline before allowing students to apply.
- **SPA with Client-side Routing:** Vue Router with history mode and a Flask catch-all route for seamless single-page navigation.

---

## Video

`<< Link to your online video of not more than 3 minutes length >>`

---
