import os
from flask import Flask, send_from_directory, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config
from models import db, User
from werkzeug.security import generate_password_hash
from flask_caching import Cache

# Initialize extensions
jwt = JWTManager()
cache = Cache()

def create_app(config_class=Config):
    app = Flask(__name__, static_folder='../frontend/dist', static_url_path='/')
    app.config.from_object(config_class)

    db.init_app(app)
    jwt.init_app(app)
    cache.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

    # Register blueprints
    from routes.auth import auth_bp
    from routes.admin import admin_bp
    from routes.company import company_bp
    from routes.student import student_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(company_bp, url_prefix='/api/company')
    app.register_blueprint(student_bp, url_prefix='/api/student')

    with app.app_context():
        db.create_all()
        _create_default_admin()

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        if path != "" and os.path.exists(app.static_folder + '/' + path):
            return send_from_directory(app.static_folder, path)
        else:
            # Fallback to index.html for Vue router to handle
            if os.path.exists(os.path.join(app.static_folder, 'index.html')):
                return send_from_directory(app.static_folder, 'index.html')
            else:
                return "Frontend not built yet. Run 'npm run build' in frontend directory."

    @app.route('/api/health')
    def health():
        return jsonify({"status": "ok"})

    return app

def _create_default_admin():
    admin = User.query.filter_by(role='admin').first()
    if not admin:
        new_admin = User(
            email='admin@institute.edu',
            password_hash=generate_password_hash('admin123'),
            role='admin'
        )
        db.session.add(new_admin)
        db.session.commit()
        print("Default admin user created: admin@institute.edu / admin123")

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
