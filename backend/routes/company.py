from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, CompanyProfile, PlacementDrive, Application

company_bp = Blueprint('company', __name__)

from functools import wraps

def company_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        import json
        current_user = json.loads(get_jwt_identity())
        if current_user.get('role') != 'company':
            return jsonify({"msg": "Companies only!"}), 403
        return fn(*args, **kwargs)
    return wrapper

@company_bp.route('/dashboard', methods=['GET'])
@company_required
def dashboard_stats():
    import json
    current_user = json.loads(get_jwt_identity())
    user = User.query.get(current_user['id'])
    company = user.company_profile

    if company.approval_status != 'approved':
        return jsonify({"msg": "Your company profile is pending approval or rejected."}), 403

    drives = PlacementDrive.query.filter_by(company_id=company.id).all()
    
    # Calculate stats
    total_drives = len(drives)
    applications_count = sum([len(d.applications) for d in drives])

    return jsonify({
        "company_name": company.name,
        "hr_contact": company.hr_contact,
        "total_drives": total_drives,
        "total_applications": applications_count
    })

@company_bp.route('/drives', methods=['GET', 'POST'])
@company_required
def manage_drives():
    import json
    current_user = json.loads(get_jwt_identity())
    user = User.query.get(current_user['id'])
    company = user.company_profile

    if company.approval_status != 'approved':
        return jsonify({"msg": "Company not approved"}), 403

    if request.method == 'POST':
        data = request.get_json()
        from datetime import datetime
        deadline_date = datetime.strptime(data.get('deadline'), "%Y-%m-%d")

        new_drive = PlacementDrive(
            company_id=company.id,
            job_title=data.get('job_title'),
            description=data.get('description'),
            min_cgpa=float(data.get('min_cgpa')),
            allowed_branches=data.get('allowed_branches'),
            deadline=deadline_date,
            salary=data.get('salary', ''),
            location=data.get('location', ''),
            status='pending'  # Admins need to approve
        )
        db.session.add(new_drive)
        db.session.commit()
        return jsonify({"msg": "Drive created and pending admin approval."}), 201
    
    # GET
    drives = PlacementDrive.query.filter_by(company_id=company.id).all()
    results = []
    for d in drives:
        results.append({
            "id": d.id,
            "job_title": d.job_title,
            "status": d.status,
            "deadline": d.deadline.strftime("%Y-%m-%d"),
            "salary": d.salary or '',
            "location": d.location or '',
            "applications_count": len(d.applications)
        })
    return jsonify(results)

@company_bp.route('/drives/<int:drive_id>/applications', methods=['GET'])
@company_required
def get_drive_applications(drive_id):
    import json
    current_user = json.loads(get_jwt_identity())
    user = User.query.get(current_user['id'])
    company = user.company_profile

    drive = PlacementDrive.query.get_or_404(drive_id)
    if drive.company_id != company.id:
        return jsonify({"msg": "Unauthorized"}), 403

    applications = Application.query.filter_by(drive_id=drive_id).all()
    results = []
    for app in applications:
        results.append({
            "id": app.id,
            "student_name": f"{app.student.first_name} {app.student.last_name}",
            "student_branch": app.student.branch,
            "student_cgpa": app.student.cgpa,
            "status": app.status,
            "applied_at": app.applied_at.isoformat(),
            "resume_url": app.student.resume_url
        })
    return jsonify(results)

@company_bp.route('/applications/<int:app_id>/status', methods=['POST'])
@company_required
def update_application_status(app_id):
    import json
    current_user = json.loads(get_jwt_identity())
    user = User.query.get(current_user['id'])
    company = user.company_profile

    application = Application.query.get_or_404(app_id)
    if application.drive.company_id != company.id:
        return jsonify({"msg": "Unauthorized"}), 403

    data = request.get_json()
    new_status = data.get('status')
    
    if new_status not in ['shortlisted', 'selected', 'rejected']:
        return jsonify({"msg": "Invalid status"}), 400

    application.status = new_status
    db.session.commit()
    return jsonify({"msg": f"Application status updated to {new_status}"})

@company_bp.route('/drives/<int:drive_id>/complete', methods=['POST'])
@company_required
def complete_drive(drive_id):
    import json
    current_user = json.loads(get_jwt_identity())
    user = User.query.get(current_user['id'])
    company = user.company_profile

    drive = PlacementDrive.query.get_or_404(drive_id)
    if drive.company_id != company.id:
        return jsonify({"msg": "Unauthorized"}), 403

    drive.status = 'closed'
    db.session.commit()
    return jsonify({"msg": "Drive marked as completed"})

@company_bp.route('/drives/<int:drive_id>/unpublish', methods=['POST'])
@company_required
def unpublish_drive(drive_id):
    import json
    current_user = json.loads(get_jwt_identity())
    user = User.query.get(current_user['id'])
    company = user.company_profile

    drive = PlacementDrive.query.get_or_404(drive_id)
    if drive.company_id != company.id:
        return jsonify({"msg": "Unauthorized"}), 403

    drive.status = 'pending'
    db.session.commit()
    return jsonify({"msg": "Drive unpublished"})
