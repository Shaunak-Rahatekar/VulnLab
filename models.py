# models.py
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    # The plain password column exists here solely so the vulnerable SQL query 
    # (which compares password='{password}') works for legitimate logins as well.
    password = db.Column(db.String(50), nullable=False) 
    password_hash = db.Column(db.String(256), nullable=False)

def seed_db():
    # Seed with dummy users if the table is empty
    if User.query.first() is None:
        user1 = User(
            username='admin', 
            password='adminpassword', 
            password_hash=generate_password_hash('adminpassword')
        )
        user2 = User(
            username='johndoe', 
            password='password123', 
            password_hash=generate_password_hash('password123')
        )
        db.session.add_all([user1, user2])
        db.session.commit()
