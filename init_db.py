"""
Initialize SQLite Database
Run: python init_db.py
"""

from main import app, db

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("✓ Database created successfully!")
        print("✓ Tables: team, service, project")
