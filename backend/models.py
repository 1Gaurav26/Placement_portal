from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False) # 'admin', 'company', 'student'
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    company_profile = db.relationship('CompanyProfile', back_populates='user', uselist=False, cascade='all, delete-orphan')
    student_profile = db.relationship('StudentProfile', back_populates='user', uselist=False, cascade='all, delete-orphan')

class CompanyProfile(db.Model):
    __tablename__ = 'company_profiles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    hr_contact = db.Column(db.String(100), nullable=False)
    website = db.Column(db.String(255), nullable=True)
    approval_status = db.Column(db.String(20), default='pending') # pending, approved, rejected

    user = db.relationship('User', back_populates='company_profile')
    drives = db.relationship('PlacementDrive', back_populates='company', cascade='all, delete-orphan')

class StudentProfile(db.Model):
    __tablename__ = 'student_profiles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    branch = db.Column(db.String(50), nullable=False)
    cgpa = db.Column(db.Float, nullable=False)
    graduation_year = db.Column(db.Integer, nullable=False)
    resume_url = db.Column(db.String(255), nullable=True)

    user = db.relationship('User', back_populates='student_profile')
    applications = db.relationship('Application', back_populates='student', cascade='all, delete-orphan')

class PlacementDrive(db.Model):
    __tablename__ = 'placement_drives'
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company_profiles.id'), nullable=False)
    job_title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    min_cgpa = db.Column(db.Float, nullable=False)
    allowed_branches = db.Column(db.String(255), nullable=False) # e.g. "CSE,ECE,IT"
    deadline = db.Column(db.DateTime, nullable=False)
    salary = db.Column(db.String(100), nullable=True)
    location = db.Column(db.String(150), nullable=True)
    status = db.Column(db.String(20), default='pending') # pending, approved, closed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    company = db.relationship('CompanyProfile', back_populates='drives')
    applications = db.relationship('Application', back_populates='drive', cascade='all, delete-orphan')

class Application(db.Model):
    __tablename__ = 'applications'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student_profiles.id'), nullable=False)
    drive_id = db.Column(db.Integer, db.ForeignKey('placement_drives.id'), nullable=False)
    status = db.Column(db.String(20), default='applied') # applied, shortlisted, selected, rejected
    interview_type = db.Column(db.String(50), default='N/A') # e.g. In-person, Online
    remark = db.Column(db.String(255), default='')
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)

    student = db.relationship('StudentProfile', back_populates='applications')
    drive = db.relationship('PlacementDrive', back_populates='applications')
