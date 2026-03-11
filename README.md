# 🎓 Placement Portal Application

A full-stack **Placement Portal** that streamlines campus recruitment by connecting **Students**, **Companies**, and the **Admin** (Training & Placement Office) on a single platform.

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Architecture](#-architecture)
- [Project Structure](#-project-structure)
- [Database Schema](#-database-schema)
- [API Endpoints](#-api-endpoints)
- [Getting Started](#-getting-started)
- [Environment Variables](#-environment-variables)
- [Celery Background Jobs](#-celery-background-jobs)
- [Default Credentials](#-default-credentials)
- [License](#-license)

---

## ✨ Features

### 🔐 Authentication & Authorization
- JWT-based authentication with role-based access control
- Three roles: **Admin**, **Company**, **Student**
- Protected routes with automatic redirection

### 👨‍💼 Admin Dashboard
- Approve / reject company registrations
- Approve / reject placement drives
- View all students, companies, and applications
- Deactivate user accounts

### 🏢 Company Portal
- Register and create a company profile (name, HR contact, website)
- Create placement drives with eligibility criteria (min CGPA, allowed branches, deadline)
- View and manage applications (shortlist / select / reject)

### 🎓 Student Portal
- Register with academic details (branch, CGPA, graduation year, resume)
- Browse approved placement drives filtered by eligibility
- Apply to drives and track application status
- Export application history to CSV (async via Celery)

### ⚙️ Background Jobs (Celery + Redis)
- **CSV Export** — Async generation of student application reports
- **Daily Deadline Reminders** — Alerts for drives expiring within 24 hours
- **Monthly Activity Report** — Automated placement statistics report

### 🚀 Performance
- Redis-backed response caching (Flask-Caching)
- Celery Beat for scheduled tasks

---

## 🛠 Tech Stack

| Layer        | Technology                                      |
|--------------|--------------------------------------------------|
| **Frontend** | Vue 3, Vite, Pinia, Vue Router, Bootstrap 5, Axios |
| **Backend**  | Flask, Flask-SQLAlchemy, Flask-JWT-Extended, Flask-CORS, Flask-Caching |
| **Database** | SQLite (default, easily swappable to PostgreSQL) |
| **Task Queue** | Celery, Redis                                 |
| **Dev Tools** | Vite Dev Server, Flask Debug Mode              |

---

## 🏗 Architecture

```
┌──────────────────────┐        ┌────────────────────────┐
│   Vue 3 Frontend     │  HTTP  │    Flask Backend        │
│   (Vite Dev Server)  │◄──────►│    REST API             │
│                      │        │                         │
│  • Pinia (State)     │        │  • JWT Auth             │
│  • Vue Router        │        │  • SQLAlchemy ORM       │
│  • Bootstrap 5       │        │  • Flask-Caching        │
│  • Axios             │        │  • Celery Tasks         │
└──────────────────────┘        └──────────┬─────────────┘
                                           │
                                ┌──────────▼─────────────┐
                                │      SQLite / DB        │
                                └──────────┬─────────────┘
                                           │
                                ┌──────────▼─────────────┐
                                │    Redis (Broker +      │
                                │    Cache + Result Store) │
                                └─────────────────────────┘
```

---

## 📁 Project Structure

```
placement/
├── backend/
│   ├── app.py                 # Flask app factory & entry point
│   ├── config.py              # Configuration (DB, JWT, Redis, Celery)
│   ├── models.py              # SQLAlchemy models
│   ├── celery_worker.py       # Celery app setup
│   ├── tasks.py               # Async & scheduled Celery tasks
│   ├── routes/
│   │   ├── auth.py            # Login, register, token endpoints
│   │   ├── admin.py           # Admin CRUD & approval endpoints
│   │   ├── company.py         # Company profile & drive management
│   │   └── student.py         # Student profile, applications, CSV export
│   └── instance/
│       └── ppa.db             # SQLite database file
│
├── frontend/
│   ├── index.html             # Vite entry HTML
│   ├── vite.config.js         # Vite configuration
│   ├── package.json           # npm dependencies
│   └── src/
│       ├── main.js            # Vue app bootstrap
│       ├── App.vue            # Root component
│       ├── style.css          # Global styles
│       ├── router/
│       │   └── index.js       # Vue Router with auth guards
│       ├── store/
│       │   └── auth.js        # Pinia auth store (JWT, role)
│       ├── components/        # Reusable UI components
│       └── views/
│           ├── Home.vue              # Landing page
│           ├── Login.vue             # Sign-in page
│           ├── RegisterStudent.vue   # Student registration
│           ├── RegisterCompany.vue   # Company registration
│           ├── admin/
│           │   └── Dashboard.vue     # Admin dashboard
│           ├── company/
│           │   └── Dashboard.vue     # Company dashboard
│           └── student/
│               └── Dashboard.vue     # Student dashboard
│
└── README.md
```

---

## 🗄 Database Schema

```
┌────────────┐    1    ┌──────────────────┐    1    ┌──────────────────┐
│   User     │────────►│ CompanyProfile   │────────►│ PlacementDrive   │
│            │         │                  │         │                  │
│ id         │         │ id               │         │ id               │
│ email      │         │ user_id (FK)     │         │ company_id (FK)  │
│ password   │         │ name             │         │ job_title        │
│ role       │         │ hr_contact       │         │ description      │
│ active     │         │ website          │         │ min_cgpa         │
│ created_at │         │ approval_status  │         │ allowed_branches │
└─────┬──────┘         └──────────────────┘         │ deadline         │
      │                                             │ status           │
      │ 1   ┌──────────────────┐                    │ created_at       │
      └────►│ StudentProfile   │                    └────────┬─────────┘
            │                  │                             │
            │ id               │    ┌──────────────────┐     │
            │ user_id (FK)     │    │   Application    │     │
            │ first_name       │◄───│                  │────►│
            │ last_name        │    │ id               │
            │ branch           │    │ student_id (FK)  │
            │ cgpa             │    │ drive_id (FK)    │
            │ graduation_year  │    │ status           │
            │ resume_url       │    │ applied_at       │
            └──────────────────┘    └──────────────────┘
```

---

## 🔌 API Endpoints

### Authentication — `/api/auth`
| Method | Endpoint              | Description               |
|--------|-----------------------|---------------------------|
| POST   | `/api/auth/login`     | Login & receive JWT token |
| POST   | `/api/auth/register`  | Register a new user       |

### Admin — `/api/admin`
| Method | Endpoint                              | Description                    |
|--------|---------------------------------------|--------------------------------|
| GET    | `/api/admin/companies`                | List all companies             |
| PUT    | `/api/admin/companies/:id/approve`    | Approve a company              |
| PUT    | `/api/admin/companies/:id/reject`     | Reject a company               |
| GET    | `/api/admin/drives`                   | List all placement drives      |
| PUT    | `/api/admin/drives/:id/approve`       | Approve a drive                |
| GET    | `/api/admin/students`                 | List all students              |
| PUT    | `/api/admin/users/:id/deactivate`     | Deactivate a user account      |

### Company — `/api/company`
| Method | Endpoint                               | Description                     |
|--------|----------------------------------------|---------------------------------|
| GET    | `/api/company/profile`                 | Get company profile             |
| GET    | `/api/company/drives`                  | List company's drives           |
| POST   | `/api/company/drives`                  | Create a new placement drive    |
| GET    | `/api/company/drives/:id/applications` | View applications for a drive   |
| PUT    | `/api/company/applications/:id`        | Update application status       |

### Student — `/api/student`
| Method | Endpoint                            | Description                        |
|--------|-------------------------------------|------------------------------------|
| GET    | `/api/student/profile`              | Get student profile                |
| GET    | `/api/student/drives`               | Browse eligible placement drives   |
| POST   | `/api/student/drives/:id/apply`     | Apply to a placement drive         |
| GET    | `/api/student/applications`         | View own applications              |
| POST   | `/api/student/export`               | Export applications CSV (async)    |

### Utility
| Method | Endpoint       | Description      |
|--------|----------------|------------------|
| GET    | `/api/health`  | Health check     |

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+**
- **Node.js 18+** & **npm**
- **Redis** (for Celery & caching)

### 1. Clone the Repository

```bash
git clone <repository-url>
cd placement
```

### 2. Backend Setup

```bash
# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# Install Python dependencies
pip install flask flask-sqlalchemy flask-jwt-extended flask-cors flask-caching celery redis werkzeug

# Start the Flask server
cd backend
python app.py
```

The backend runs at **http://localhost:5000**.

### 3. Frontend Setup

```bash
# In a new terminal
cd frontend

# Install npm dependencies
npm install

# Start Vite dev server
npm run dev
```

The frontend runs at **http://localhost:5173**.

### 4. Start Celery Worker (optional, for background jobs)

```bash
# Ensure Redis is running, then in a new terminal
cd backend
celery -A celery_worker.celery_app worker --loglevel=info

# For scheduled tasks (Celery Beat)
celery -A celery_worker.celery_app beat --loglevel=info
```

### 5. Build for Production

```bash
cd frontend
npm run build
# The built assets are served by Flask from frontend/dist/
```

---

## 🔧 Environment Variables

| Variable          | Default                         | Description                 |
|-------------------|---------------------------------|-----------------------------|
| `SECRET_KEY`      | `dev-secret-key-ppa`            | Flask secret key            |
| `DATABASE_URL`    | `sqlite:///ppa.db`              | Database connection URI     |
| `JWT_SECRET_KEY`  | `jwt-secret-key-ppa`            | JWT signing secret          |
| `CELERY_BROKER_URL` | `redis://localhost:6379/0`    | Celery broker URL           |
| `CELERY_RESULT_BACKEND` | `redis://localhost:6379/1` | Celery result backend URL   |

---

## ⏰ Celery Background Jobs

| Task                          | Trigger                        | Description                                   |
|-------------------------------|--------------------------------|-----------------------------------------------|
| `export_student_applications_csv` | User-triggered (POST `/api/student/export`) | Generates a CSV of a student's applications |
| `daily_deadline_reminders`    | Scheduled — daily at 8:00 AM   | Alerts for drives expiring within 24 hours    |
| `monthly_activity_report`     | Scheduled — monthly (every 60s in dev) | Generates placement statistics report    |

---

## 🔑 Default Credentials

On first run, a default admin account is created automatically:

| Field    | Value                  |
|----------|------------------------|
| Email    | `admin@institute.edu`  |
| Password | `admin123`             |
| Role     | Admin                  |

> ⚠️ **Change these credentials immediately in production!**

---

## 📄 License

This project is developed for academic/educational purposes.
