"""
Database reset script using application context
"""
import os
import shutil
from app import create_app
from models import db
from models.user import User
from models.question import Question
from models.question_paper import QuestionPaper
from werkzeug.security import generate_password_hash

def reset_database():
    print("Resetting database...")
    
    # Remove old database file if possible
    db_path = os.path.join('instance', 'question_bank.db')
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
            print(f"✓ Removed old database: {db_path}")
        except PermissionError:
            print(f"⚠ Could not remove database file (locked). Proceeding with drop_all()...")
        except Exception as e:
            print(f"⚠ Error removing database file: {e}")

    app = create_app()
    with app.app_context():
        # Drop all tables first (in case file deletion failed)
        db.drop_all()
        print("✓ Dropped all existing tables")
        
        # Create all tables based on models
        db.create_all()
        print("✓ Created database tables from models")
        
        # Seed users
        admin = User(
            username='admin',
            email='admin@example.com',
            password_hash=generate_password_hash('admin123'),
            role='Admin'
        )
        
        faculty = User(
            username='faculty',
            email='faculty@example.com',
            password_hash=generate_password_hash('faculty123'),
            role='Faculty'
        )
        
        db.session.add(admin)
        db.session.add(faculty)
        db.session.commit()
        
        print("✓ Created default users")
        print("\n" + "="*60)
        print("Database Reset Complete!")
        print("="*60)
        print("\nDefault Credentials:")
        print("  Admin:   username='admin'   password='admin123'")
        print("  Faculty: username='faculty' password='faculty123'")
        print("\n✓ You can now login to the application!")
        print("="*60)

if __name__ == "__main__":
    reset_database()
