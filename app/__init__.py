from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_name='config'):
    """Application factory function"""
    app = Flask(__name__)
    app.config.from_object(config_name)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    
    # Create upload folder if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.lecturer import lecturer_bp
    from app.routes.student import student_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(lecturer_bp)
    app.register_blueprint(student_bp)
    
    # Main route
    @app.route('/')
    def index():
        from flask import render_template
        return render_template('index.html')
    
    # Load user for login manager
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))
    return app
