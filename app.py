"""
Main Flask Application
Dynamic Question Paper Generator using Bloom's Taxonomy
"""

from flask import Flask
from flask_login import LoginManager
from config import Config
from models import db
from models.user import User
from routes.auth import auth_bp, login_manager
from routes.main import main_bp
from routes.questions import questions_bp
from routes.paper import paper_bp
import os

def create_app(config_class=Config):
    """Application factory"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(questions_bp)
    app.register_blueprint(paper_bp)
    
    # Create upload folder if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    print("=" * 60)
    print("Dynamic Question Paper Generator")
    print("=" * 60)
    print("Server starting on http://127.0.0.1:5000")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)
