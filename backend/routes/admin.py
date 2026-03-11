from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, CompanyProfile, PlacementDrive, StudentProfile, Application

admin_bp = Blueprint('admin', __name__)

from functools import wraps

def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        import json
        current_user = json.loads(get_jwt_identity())
        if current_user.get('role') != 'admin':
            return jsonify({"msg": "Admins only!"}), 403
        return fn(*args, **kwargs)
    return wrapper

@admin_bp.route('/dashboard', methods=['GET'])
@admin_required
def dashboard_stats():
    total_students = User.query.filter_by(role='student').count()
    total_companies = User.query.filter_by(role='company').count()
    total_drives = PlacementDrive.query.count()
    return jsonify({
        "total_students": total_students,
        "total_companies": total_companies,
        "total_drives": total_drives
    })

@admin_bp.route('/companies', methods=['GET'])
@admin_required
def get_companies():
    companies = CompanyProfile.query.all()
    results = []
    for c in companies:
        results.append({
            "id": c.id,
            "name": c.name,
            "hr_contact": c.hr_contact,
            "website": c.website,
            "approval_status": c.approval_status,
            "active": c.user.active,
            "user_id": c.user.id
        })
    return jsonify(results)

@admin_bp.route('/companies/<int:company_id>/approve', methods=['POST'])
@admin_required
def approve_company(company_id):
    company = CompanyProfile.query.get_or_404(company_id)
    company.approval_status = 'approved'
    db.session.commit()
    return jsonify({"msg": "Company approved"})

@admin_bp.route('/companies/<int:company_id>/reject', methods=['POST'])
@admin_required
def reject_company(company_id):
    company = CompanyProfile.query.get_or_404(company_id)
    company.approval_status = 'rejected'
    db.session.commit()
    return jsonify({"msg": "Company rejected"})

@admin_bp.route('/drives', methods=['GET'])
@admin_required
def get_drives():
    drives = PlacementDrive.query.all()
    results = []
    for d in drives:
        results.append({
            "id": d.id,
            "company_name": d.company.name,
            "job_title": d.job_title,
            "status": d.status,
            "deadline": d.deadline.isoformat()
        })
    return jsonify(results)

@admin_bp.route('/drives/<int:drive_id>/approve', methods=['POST'])
@admin_required
def approve_drive(drive_id):
    drive = PlacementDrive.query.get_or_404(drive_id)
    drive.status = 'approved'
    db.session.commit()
    return jsonify({"msg": "Drive approved"})

@admin_bp.route('/drives/<int:drive_id>/reject', methods=['POST'])
@admin_required
def reject_drive(drive_id):
    drive = PlacementDrive.query.get_or_404(drive_id)
    drive.status = 'rejected'
    db.session.commit()
    return jsonify({"msg": "Drive rejected"})

@admin_bp.route('/users/<int:user_id>/toggle_status', methods=['POST'])
@admin_required
def toggle_user_status(user_id):
    user = User.query.get_or_404(user_id)
    if user.role == 'admin':
        return jsonify({"msg": "Cannot deactivate admin"}), 400
    user.active = not user.active
    db.session.commit()
    return jsonify({"msg": f"User active status changed to {user.active}"})

@admin_bp.route('/students', methods=['GET'])
@admin_required
def get_students():
    students = StudentProfile.query.all()
    results = []
    for s in students:
        results.append({
            "id": s.id,
            "first_name": s.first_name,
            "last_name": s.last_name,
            "branch": s.branch,
            "cgpa": s.cgpa,
            "graduation_year": s.graduation_year,
            "email": s.user.email,
            "active": s.user.active,
            "user_id": s.user.id
        })
    return jsonify(results)

@admin_bp.route('/applications', methods=['GET'])
@admin_required
def get_all_applications():
    applications = Application.query.all()
    results = []
    for app in applications:
        results.append({
            "id": app.id,
            "student_name": f"{app.student.first_name} {app.student.last_name}",
            "company_name": app.drive.company.name,
            "job_title": app.drive.job_title,
            "status": app.status,
            "interview_type": app.interview_type,
            "remark": app.remark,
            "applied_at": app.applied_at.isoformat()
        })
    return jsonify(results)

@admin_bp.route('/drives/<int:drive_id>/complete', methods=['POST'])
@admin_required
def complete_drive(drive_id):
    drive = PlacementDrive.query.get_or_404(drive_id)
    drive.status = 'closed'
    db.session.commit()
    return jsonify({"msg": "Drive marked as completed"})

@admin_bp.route('/search', methods=['GET'])
@admin_required
def search():
    q = request.args.get('q', '').strip()
    if not q:
        return jsonify({"students": [], "companies": []})

    students = StudentProfile.query.filter(
        db.or_(
            StudentProfile.first_name.ilike(f'%{q}%'),
            StudentProfile.last_name.ilike(f'%{q}%')
        )
    ).all()

    companies = CompanyProfile.query.filter(
        CompanyProfile.name.ilike(f'%{q}%')
    ).all()

    return jsonify({
        "students": [{
            "id": s.id,
            "name": f"{s.first_name} {s.last_name}",
            "branch": s.branch,
            "cgpa": s.cgpa
        } for s in students],
        "companies": [{
            "id": c.id,
            "name": c.name,
            "approval_status": c.approval_status
        } for c in companies]
    })
