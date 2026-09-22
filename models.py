# models.py
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from datetime import datetime

# In-memory server-side session storage to demonstrate Fixation.
# Keys are session IDs, values are dicts containing user data.
server_sessions = {}

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    profile_pic = db.Column(db.String(255), nullable=True)
    password_hash = db.Column(db.String(120), nullable=False)

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

def seed_db():
    # Seed with dummy users if the table is empty
    if User.query.first() is None:
        user1 = User(
            username='admin', 
            email='admin@vulnlab.local',
            password_hash=generate_password_hash('adminpassword')
        )
        user2 = User(
            username='johndoe', 
            email='john@vulnlab.local',
            password_hash=generate_password_hash('password123')
        )
        db.session.add_all([user1, user2])
        db.session.commit()

    # Seed products if empty
    if Product.query.first() is None:
        p1 = Product(name='Secure Router', price=199.99, description='A very secure home router with default passwords changed.')
        p2 = Product(name='Hacker Keyboard', price=75.50, description='Mechanical keyboard for typing payloads fast.')
        p3 = Product(name='Privacy Screen', price=25.00, description='Keep prying eyes away from your terminal.')
        p4 = Product(name='VPN Subscription (1 Yr)', price=49.99, description='Anonymous browsing for your whole family.')
        p5 = Product(name='Webcam Cover', price=5.99, description='Stop hackers from watching you.')
        p6 = Product(name='Faraday Bag', price=30.00, description='Block all wireless signals from your devices.')
        db.session.add_all([p1, p2, p3, p4, p5, p6])
        db.session.commit()
