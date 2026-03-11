from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, PlacementDrive, Application

student_bp = Blueprint('student', __name__)

from functools import wraps

def student_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        import json
        current_user = json.loads(get_jwt_identity())
        if current_user.get('role') != 'student':
            return jsonify({"msg": "Students only!"}), 403
        return fn(*args, **kwargs)
    return wrapper

from app import cache

@student_bp.route('/dashboard', methods=['GET'])
@student_required
@cache.cached(timeout=60, key_prefix=lambda: f"student_dashboard_{json.loads(get_jwt_identity())['id']}")
def dashboard():
    import json
    current_user = json.loads(get_jwt_identity())
    user = User.query.get(current_user['id'])
    student = user.student_profile
    
    # Get all approved drives
    approved_drives = PlacementDrive.query.filter_by(status='approved').all()
    
    # Check student applied drives
    applied_drive_ids = [app.drive_id for app in student.applications]

    results = []
    for d in approved_drives:
        eligibility = True
        reason = ""
        if student.cgpa < d.min_cgpa:
            eligibility = False
            reason = "Low CGPA"
        
        allowed = [b.strip().upper() for b in d.allowed_branches.split(',')]
        if student.branch.upper() not in allowed and "ANY" not in allowed:
            eligibility = False
            reason = "Branch not allowed"

        import datetime
        if datetime.datetime.utcnow() > d.deadline:
            eligibility = False
            reason = "Deadline passed"

        results.append({
            "id": d.id,
            "company_name": d.company.name,
            "job_title": d.job_title,
            "description": d.description,
            "deadline": d.deadline.strftime("%Y-%m-%d"),
            "is_eligible": eligibility,
            "ineligibility_reason": reason,
            "has_applied": d.id in applied_drive_ids
        })
    return jsonify(results)

@student_bp.route('/drives/<int:drive_id>/apply', methods=['POST'])
@student_required
def apply_drive(drive_id):
    import json
    current_user = json.loads(get_jwt_identity())
    user = User.query.get(current_user['id'])
    student = user.student_profile

    # Check if already applied
    if Application.query.filter_by(student_id=student.id, drive_id=drive_id).first():
        return jsonify({"msg": "Already applied to this drive"}), 400

    drive = PlacementDrive.query.get_or_404(drive_id)
    if drive.status != 'approved':
        return jsonify({"msg": "Drive not available"}), 400

    new_app = Application(
        student_id=student.id,
        drive_id=drive.id,
        status='applied'
    )
    db.session.add(new_app)
    db.session.commit()
    return jsonify({"msg": "Successfully applied"}), 201

@student_bp.route('/applications', methods=['GET'])
@student_required
def get_applications():
    import json
    current_user = json.loads(get_jwt_identity())
    user = User.query.get(current_user['id'])
    student = user.student_profile

    apps = Application.query.filter_by(student_id=student.id).all()
    results = []
    for app in apps:
        results.append({
            "id": app.id,
            "company_name": app.drive.company.name,
            "job_title": app.drive.job_title,
            "status": app.status,
            "interview_type": app.interview_type,
            "remark": app.remark,
            "applied_at": app.applied_at.isoformat()
        })
    return jsonify(results)

@student_bp.route('/profile', methods=['GET', 'PUT'])
@student_required
def profile():
    import json
    current_user = json.loads(get_jwt_identity())
    user = User.query.get(current_user['id'])
    student = user.student_profile

    if request.method == 'PUT':
        data = request.get_json()
        student.first_name = data.get('first_name', student.first_name)
        student.last_name = data.get('last_name', student.last_name)
        student.branch = data.get('branch', student.branch)
        if data.get('cgpa'):
            student.cgpa = float(data.get('cgpa'))
        student.resume_url = data.get('resume_url', student.resume_url)
        db.session.commit()
        return jsonify({"msg": "Profile updated"})

    return jsonify({
        "first_name": student.first_name,
        "last_name": student.last_name,
        "branch": student.branch,
        "cgpa": student.cgpa,
        "graduation_year": student.graduation_year,
        "email": user.email,
        "resume_url": student.resume_url
    })

@student_bp.route('/companies', methods=['GET'])
@student_required
def get_companies():
    from models import CompanyProfile
    companies = CompanyProfile.query.filter_by(approval_status='approved').all()
    results = []
    for c in companies:
        results.append({
            "id": c.id,
            "name": c.name,
            "hr_contact": c.hr_contact,
            "website": c.website
        })
    return jsonify(results)

@student_bp.route('/companies/<int:company_id>', methods=['GET'])
@student_required
def get_company_detail(company_id):
    from models import CompanyProfile
    company = CompanyProfile.query.get_or_404(company_id)
    drives = PlacementDrive.query.filter_by(company_id=company.id, status='approved').all()
    return jsonify({
        "id": company.id,
        "name": company.name,
        "hr_contact": company.hr_contact,
        "website": company.website,
        "drives": [{
            "id": d.id,
            "job_title": d.job_title,
            "description": d.description,
            "min_cgpa": d.min_cgpa,
            "allowed_branches": d.allowed_branches,
            "deadline": d.deadline.strftime("%Y-%m-%d"),
            "salary": d.salary or '',
            "location": d.location or ''
        } for d in drives]
    })

@student_bp.route('/drives/<int:drive_id>', methods=['GET'])
@student_required
def get_drive_detail(drive_id):
    drive = PlacementDrive.query.get_or_404(drive_id)
    import json
    current_user = json.loads(get_jwt_identity())
    user = User.query.get(current_user['id'])
    student = user.student_profile
    has_applied = Application.query.filter_by(student_id=student.id, drive_id=drive_id).first() is not None
    return jsonify({
        "id": drive.id,
        "company_name": drive.company.name,
        "company_id": drive.company.id,
        "job_title": drive.job_title,
        "description": drive.description,
        "min_cgpa": drive.min_cgpa,
        "allowed_branches": drive.allowed_branches,
        "deadline": drive.deadline.strftime("%Y-%m-%d"),
        "salary": drive.salary or '',
        "location": drive.location or '',
        "has_applied": has_applied
    })

@student_bp.route('/tasks/export-csv', methods=['POST'])
@student_required
def export_csv_route():
    import json
    current_user = json.loads(get_jwt_identity())
    user = User.query.get(current_user['id'])
    student = user.student_profile
    
    from tasks import export_student_applications_csv
    export_student_applications_csv.delay(student.id, user.email)
    
    return jsonify({"msg": "CSV Export triggered successfully! You will receive an alert once done."})
