from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, CompanyProfile, StudentProfile

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"msg": "Bad email or password"}), 401

    if not user.active:
        return jsonify({"msg": "Account is deactivated"}), 403

    import json
    access_token = create_access_token(identity=json.dumps({'id': user.id, 'role': user.role}))
    return jsonify(access_token=access_token, role=user.role)

@auth_bp.route('/register/student', methods=['POST'])
def register_student():
    data = request.get_json()
    if User.query.filter_by(email=data.get('email')).first():
        return jsonify({"msg": "Email already registered"}), 400

    new_user = User(
        email=data.get('email'),
        password_hash=generate_password_hash(data.get('password')),
        role='student'
    )
    db.session.add(new_user)
    db.session.flush()

    student_profile = StudentProfile(
        user_id=new_user.id,
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        branch=data.get('branch'),
        cgpa=float(data.get('cgpa')),
        graduation_year=int(data.get('graduation_year'))
    )
    db.session.add(student_profile)
    db.session.commit()

    return jsonify({"msg": "Student registered successfully"}), 201

@auth_bp.route('/register/company', methods=['POST'])
def register_company():
    data = request.get_json()
    if User.query.filter_by(email=data.get('email')).first():
        return jsonify({"msg": "Email already registered"}), 400

    new_user = User(
        email=data.get('email'),
        password_hash=generate_password_hash(data.get('password')),
        role='company'
    )
    db.session.add(new_user)
    db.session.flush()

    company_profile = CompanyProfile(
        user_id=new_user.id,
        name=data.get('company_name'),
        hr_contact=data.get('hr_contact'),
        website=data.get('website', ''),
        approval_status='pending'  # Admin must approve
    )
    db.session.add(company_profile)
    db.session.commit()

    return jsonify({"msg": "Company registered and pending admin approval"}), 201
